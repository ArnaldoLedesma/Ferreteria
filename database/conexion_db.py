import sqlite3
import csv # libreria y herramienta para leer y escribir archivos de csv
from datetime import date, datetime

class ConexionDB:
    def __init__(self, nombre_bd="ferreteria.db"):
        self.nombre_bd = nombre_bd

    def conectar(self): # def SON METODOS NUEVOS DENTRO DE LA CLASE
        return sqlite3.connect(self.nombre_bd)

    def insertar_producto(self, codigo, nombre, precio_lista, precio_c_iva, stock, proveedor):
        connexion = self.conectar()
        cursor = connexion.cursor()
        hoy = date.today().strftime("%d/%m/%Y")
        cursor.execute(
            "INSERT INTO Productos (codigo, nombre, precio_lista, precio_c_iva, precio_final, stock, proveedor, fecha_act) VALUES (?, ?, ?, ?, 0, ?, ?, ?)",
            (codigo, nombre, precio_lista, precio_c_iva, stock, proveedor, hoy)
        )
        connexion.commit()
        connexion.close()

    def obtener_productos(self):
        connexion = self.conectar()
        cursor = connexion.cursor()
        cursor.execute("SELECT * FROM Productos")
        datos = cursor.fetchall()
        connexion.close()
        return datos #devolvemos la lista completa donde llamaron el metodo

    def actualizar_producto(self, id_producto, codigo, nombre, precio_lista, precio_c_iva, stock, proveedor):
        connexion = self.conectar()
        cursor = connexion.cursor()
        hoy = date.today().strftime("%d/%m/%Y")
        cursor.execute("""
            UPDATE Productos
            SET codigo = ?, nombre = ?, precio_lista = ?, precio_c_iva = ?, stock = ?, proveedor = ?, fecha_act = ?
            WHERE id = ?
        """, (codigo, nombre, precio_lista, precio_c_iva, stock, proveedor, hoy, id_producto))
        connexion.commit()
        connexion.close()

    def eliminar_producto(self, id_producto):
        connexion = self.conectar()
        cursor = connexion.cursor()
        cursor.execute("DELETE FROM Productos WHERE id = ?", (id_producto,))
        connexion.commit()
        connexion.close() 

    def actualizar_precios_pol(self, ruta_csv):
        connexion = self.conectar()
        hoy = date.today().strftime("%d/%m/%Y")

        resumen = {
            "actualizados": 0,
            "nuevos": 0,
            "ausentes": 0,
            "errores": 0,
            "duplicados": 0,
        }

        codigos_csv = set()
        ids_actualizados = set()

        try:
            cursor = connexion.cursor()

            # Guarda los IDs de los productos de POL antes de importar.
            cursor.execute(
                "SELECT id FROM Productos WHERE proveedor = ?",
                ("POL",)
            )
            ids_base = {id_producto for (id_producto,) in cursor.fetchall()}

            with open(ruta_csv, encoding="latin-1", newline="") as archivo:
                lector = csv.reader(archivo)
                empezar = False

                for fila in lector:
                    if not empezar:
                        if fila and fila[0].strip().upper() == "CODIGO":
                            empezar = True
                        continue

                    if len(fila) < 5:
                        resumen["errores"] += 1
                        continue

                    codigo = fila[0].strip()
                    nombre = fila[1].strip()
                    precio_lista = fila[2].replace(",", ".").strip()
                    precio_c_iva = fila[4].replace(",", ".").strip()

                    if not codigo or not precio_c_iva:
                        resumen["errores"] += 1
                        continue

                    if codigo in codigos_csv:
                        resumen["duplicados"] += 1
                        continue

                    codigos_csv.add(codigo)

                    cursor.execute(
                        "SELECT id FROM Productos WHERE codigo = ? AND proveedor = ?",
                        (codigo, "POL")
                    )
                    existe = cursor.fetchone()

                    if existe:
                        id_producto = existe[0]
                        cursor.execute(
                            """
                            UPDATE Productos
                            SET nombre = ?, precio_lista = ?, precio_c_iva = ?,
                                fecha_act = ?
                            WHERE id = ?
                            """,
                            (nombre, precio_lista, precio_c_iva, hoy, id_producto)
                        )
                        resumen["actualizados"] += 1
                        ids_actualizados.add(id_producto)
                    else:
                        cursor.execute(
                            """
                            INSERT INTO Productos (
                                codigo, nombre, precio_lista, precio_c_iva,
                                precio_final, stock, proveedor, fecha_act
                            )
                            VALUES (?, ?, ?, ?, 0, 0, ?, ?)
                            """,
                            (codigo, nombre, precio_lista, precio_c_iva, "POL", hoy)
                        )
                        resumen["nuevos"] += 1

            if not empezar:
                raise ValueError("No se encontró el encabezado CODIGO en el CSV.")

            if not codigos_csv:
                raise ValueError("El CSV no contiene filas de productos utilizables.")

            # Los productos que no se actualizaron se cuentan, pero no se modifican.
            resumen["ausentes"] = len(ids_base - ids_actualizados)

            connexion.commit()
            return resumen

        except Exception:
            connexion.rollback()
            raise

        finally:
            connexion.close()
    def actualizar_precios_fgp(self, ruta_csv):
            resumen = dict(actualizados=0, nuevos=0, ausentes=0, errores=0, duplicados=0)
            codigos_csv = set()
            hoy = date.today().strftime("%d/%m/%Y")
            connexion = self.conectar()

            try:
                cursor = connexion.cursor()
                cursor.execute(
                    "SELECT id FROM Productos WHERE proveedor = ?",
                    ("FGP",)
                )
                ids_base = {id_producto for (id_producto,) in cursor.fetchall()}
                ids_actualizados = set()

                with open(ruta_csv, encoding="latin-1", newline="") as archivo:
                    lector = csv.reader(archivo)
                    empezar = False

                    for fila in lector:
                        if not empezar:
                            if fila and fila[0].strip().upper() == "CODIGO":
                                empezar = True
                            continue

                        if len(fila) < 6:
                            resumen["errores"] += 1
                            continue

                        codigo = fila[0].strip()
                        nombre = fila[2].strip()
                        precio_lista = fila[3].replace(",", ".").strip()
                        precio_c_iva = fila[5].replace(",", ".").strip()

                        if not codigo or not precio_c_iva:
                            resumen["errores"] += 1
                            continue

                        if codigo in codigos_csv:
                            resumen["duplicados"] += 1
                            continue

                        codigos_csv.add(codigo)
                        cursor.execute(
                            "SELECT id FROM Productos WHERE codigo = ? AND proveedor = ?",
                            (codigo, "FGP")
                        )
                        existe = cursor.fetchone()

                        if existe:
                            id_producto = existe[0]
                            cursor.execute(
                                """
                                UPDATE Productos
                                SET nombre = ?, precio_lista = ?, precio_c_iva = ?,
                                    fecha_act = ?
                                WHERE id = ?
                                """,
                                (nombre, precio_lista, precio_c_iva, hoy, id_producto)
                            )
                            resumen["actualizados"] += 1
                            ids_actualizados.add(id_producto)
                        else:
                            cursor.execute(
                                """
                                INSERT INTO Productos (
                                    codigo, nombre, precio_lista, precio_c_iva,
                                    precio_final, stock, proveedor, fecha_act
                                )
                                VALUES (?, ?, ?, ?, 0, 0, ?, ?)
                                """,
                                (codigo, nombre, precio_lista, precio_c_iva, "FGP", hoy)
                            )
                            resumen["nuevos"] += 1

                if not empezar:
                    raise ValueError("No se encontró el encabezado CODIGO en el CSV.")

                if not codigos_csv:
                    raise ValueError("El CSV no contiene filas de productos utilizables.")

                # Compara IDs para que 00101 y 101 no produzcan un falso ausente.
                resumen["ausentes"] = len(ids_base - ids_actualizados)
                connexion.commit()
                return resumen

            except Exception:
                connexion.rollback()
                raise
            finally:
                connexion.close()
    def actualizar_precios_day(self, ruta_csv):
        resumen = dict(actualizados=0, nuevos=0, ausentes=0, errores=0, duplicados=0)
        nombres_csv = set()
        ids_actualizados = set()
        hoy = date.today().strftime("%d/%m/%Y")
        connexion = self.conectar()

        try:
            cursor = connexion.cursor()
            cursor.execute(
                "SELECT id FROM Productos WHERE proveedor = ?",
                ("DAY",)
            )
            ids_base = {id_producto for (id_producto,) in cursor.fetchall()}

            with open(ruta_csv, encoding="latin-1", newline="") as archivo:
                lector = csv.reader(archivo)
                empezar = False

                for fila in lector:
                    if not empezar:
                        if fila and fila[0].strip().upper() == "MARCA":
                            empezar = True
                        continue

                    if len(fila) < 4:
                        resumen["errores"] += 1
                        continue

                    nombre = fila[1].strip()
                    precio = fila[3].replace(",", ".").strip()

                    if not nombre or not precio:
                        resumen["errores"] += 1
                        continue

                    # DAY identifica por nombre: se procesa la primera fila válida.
                    if nombre in nombres_csv:
                        resumen["duplicados"] += 1
                        continue

                    nombres_csv.add(nombre)
                    cursor.execute(
                        "SELECT id FROM Productos WHERE nombre = ? AND proveedor = ?",
                        (nombre, "DAY")
                    )
                    existe = cursor.fetchone()

                    if existe:
                        id_producto = existe[0]
                        cursor.execute(
                            """
                            UPDATE Productos
                            SET precio_lista = ?, precio_c_iva = ?, fecha_act = ?
                            WHERE id = ?
                            """,
                            (precio, precio, hoy, id_producto)
                        )
                        ids_actualizados.add(id_producto)
                        resumen["actualizados"] += 1
                    else:
                        cursor.execute(
                            """
                            INSERT INTO Productos (
                                codigo, nombre, precio_lista, precio_c_iva,
                                precio_final, stock, proveedor, fecha_act
                            )
                            VALUES (?, ?, ?, ?, 0, 0, ?, ?)
                            """,
                            ("", nombre, precio, precio, "DAY", hoy)
                        )
                        resumen["nuevos"] += 1

            if not empezar:
                raise ValueError("No se encontró el encabezado MARCA en el CSV.")

            if not nombres_csv:
                raise ValueError("El CSV no contiene filas de productos utilizables.")

            # Cuenta los registros anteriores que quedaron sin actualizar.
            resumen["ausentes"] = len(ids_base - ids_actualizados)
            connexion.commit()
            return resumen

        except Exception:
            connexion.rollback()
            raise
        finally:
            connexion.close()

    def actualizar_precios_grays(self, ruta_csv):
        resumen = dict(actualizados=0, nuevos=0, ausentes=0, errores=0, duplicados=0)
        codigos_csv = set()
        ids_actualizados = set()
        hoy = date.today().strftime("%d/%m/%Y")
        connexion = self.conectar()

        try:
            cursor = connexion.cursor()
            cursor.execute(
                "SELECT id FROM Productos WHERE proveedor = ?",
                ("GRAYS",)
            )
            ids_base = {id_producto for (id_producto,) in cursor.fetchall()}

            with open(ruta_csv, encoding="latin-1", newline="") as archivo:
                lector = csv.reader(archivo)
                empezar = False

                for fila in lector:
                    if not empezar:
                        if fila and fila[0].strip().upper() == "CODIGO FLEXXUS":
                            empezar = True
                        continue

                    if len(fila) < 6:
                        resumen["errores"] += 1
                        continue

                    codigo = fila[0].strip()
                    nombre = fila[1].strip()
                    precio = fila[5].replace(",", ".").strip()

                    if not codigo or not precio:
                        resumen["errores"] += 1
                        continue

                    if codigo in codigos_csv:
                        resumen["duplicados"] += 1
                        continue

                    codigos_csv.add(codigo)
                    cursor.execute(
                        "SELECT id FROM Productos WHERE codigo = ? AND proveedor = ?",
                        (codigo, "GRAYS")
                    )
                    existe = cursor.fetchone()

                    if existe:
                        id_producto = existe[0]
                        cursor.execute(
                            """
                            UPDATE Productos
                            SET nombre = ?, precio_lista = ?, precio_c_iva = ?,
                                fecha_act = ?
                            WHERE id = ?
                            """,
                            (nombre, precio, precio, hoy, id_producto)
                        )
                        ids_actualizados.add(id_producto)
                        resumen["actualizados"] += 1
                    else:
                        cursor.execute(
                            """
                            INSERT INTO Productos (
                                codigo, nombre, precio_lista, precio_c_iva,
                                precio_final, stock, proveedor, fecha_act
                            )
                            VALUES (?, ?, ?, ?, 0, 0, ?, ?)
                            """,
                            (codigo, nombre, precio, precio, "GRAYS", hoy)
                        )
                        resumen["nuevos"] += 1

            if not empezar:
                raise ValueError("No se encontró el encabezado CODIGO FLEXXUS en el CSV.")

            if not codigos_csv:
                raise ValueError("El CSV no contiene filas de productos utilizables.")

            # Cuenta los productos anteriores que no se actualizaron, sin tocarlos.
            resumen["ausentes"] = len(ids_base - ids_actualizados)
            connexion.commit()
            return resumen

        except Exception:
            connexion.rollback()
            raise
        finally:
            connexion.close()

    def aplicar_margen(self, proveedor, margen):
        from math import isfinite

        # Acepta 1, 1%, 1,1, 1.1, 1,1% y 1.1%.
        texto = str(margen).strip()
        if texto.endswith("%"):
            texto = texto[:-1].strip()
        texto = texto.replace(",", ".")

        try:
            porcentaje = float(texto)
        except ValueError:
            raise ValueError("Ingresá un porcentaje válido, por ejemplo 1,1%.") from None

        if not isfinite(porcentaje) or porcentaje < 0:
            raise ValueError("Ingresá un porcentaje mayor o igual a cero.")

        # Ejemplo: 3% → factor 1.03.
        factor = 1 + porcentaje / 100

        connexion = self.conectar()
        try:
            with connexion:
                connexion.execute("""
                    UPDATE Productos
                    SET precio_final = ROUND(precio_c_iva * ?, 2)
                    WHERE proveedor = ?
                """, (factor, proveedor.strip().upper()))
        finally:
            connexion.close()

    def buscar_productos_venta(self, texto=""):
        connexion = self.conectar()
        cursor = connexion.cursor()

        busqueda = f"%{texto}%"

        cursor.execute(
            """
            SELECT id, codigo, nombre, precio_final, stock
            FROM Productos
            WHERE (
                CAST(codigo AS TEXT) LIKE ?
                OR nombre LIKE ?
            )
            AND precio_final > 0
            ORDER BY nombre
            LIMIT 200
            """,
            (busqueda, busqueda)
        )  # Limita los resultados para no cargar los 21.967 productos de golpe

        productos = cursor.fetchall()
        connexion.close()

        return productos
    
    def crear_tablas_ventas(self):
        connexion = self.conectar()
        cursor = connexion.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Ventas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha TEXT NOT NULL,
                total REAL NOT NULL,
                medio_pago TEXT NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS DetalleVenta (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                venta_id INTEGER NOT NULL,
                producto_id INTEGER NOT NULL,
                codigo TEXT,
                nombre TEXT NOT NULL,
                cantidad INTEGER NOT NULL,
                precio_unitario REAL NOT NULL,
                subtotal REAL NOT NULL,
                FOREIGN KEY (venta_id) REFERENCES Ventas(id),
                FOREIGN KEY (producto_id) REFERENCES Productos(id)
            )
        """)

        connexion.commit()
        connexion.close()

    def registrar_venta(self, carrito, medio_pago):
        conexion = self.conectar()
        cursor = conexion.cursor()

        try:
            total_venta = sum(
                producto["cantidad"] * producto["precio"]
                for producto in carrito.values()
            )

            # Comprueba nuevamente el stock directamente en la base de datos
            for id_producto, producto in carrito.items():
                cursor.execute(
                    "SELECT stock FROM Productos WHERE id = ?",
                    (int(id_producto),)
                )
                resultado = cursor.fetchone()

                if resultado is None:
                    raise ValueError(
                        f'El producto "{producto["nombre"]}" ya no existe.'
                    )

                if resultado[0] < producto["cantidad"]:
                    raise ValueError(
                        f'Stock insuficiente para "{producto["nombre"]}". '
                        f'Disponible: {resultado[0]}'
                    )

            fecha_venta = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

            cursor.execute(
                """
                INSERT INTO Ventas (fecha, total, medio_pago)
                VALUES (?, ?, ?)
                """,
                (fecha_venta, total_venta, medio_pago)
            )

            venta_id = cursor.lastrowid

            for id_producto, producto in carrito.items():
                subtotal = producto["cantidad"] * producto["precio"]

                cursor.execute(
                    """
                    INSERT INTO DetalleVenta (
                        venta_id, producto_id, codigo, nombre,
                        cantidad, precio_unitario, subtotal
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        venta_id,
                        int(id_producto),
                        producto["codigo"],
                        producto["nombre"],
                        producto["cantidad"],
                        producto["precio"],
                        subtotal
                    )
                )

                cursor.execute(
                    """
                    UPDATE Productos
                    SET stock = stock - ?
                    WHERE id = ? AND stock >= ?
                    """,
                    (
                        producto["cantidad"],
                        int(id_producto),
                        producto["cantidad"]
                    )
                )

                # rowcount permite comprobar que realmente se descontó el stock
                if cursor.rowcount != 1:
                    raise ValueError(
                        f'No se pudo actualizar el stock de '
                        f'"{producto["nombre"]}".'
                    )

            conexion.commit()  # Confirma todos los cambios juntos
            return venta_id

        except Exception:
            conexion.rollback()  # Si algo falla, cancela toda la venta
            raise

        finally:
            conexion.close()