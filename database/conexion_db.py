import sqlite3
import csv # libreria y herramienta para leer y escribir archivos de csv

class ConexionDB:
    def __init__(self, nombre_bd="ferreteria.db"):
        self.nombre_bd = nombre_bd

    def conectar(self): # def SON METODOS NUEVOS DENTRO DE LA CLASE
        return sqlite3.connect(self.nombre_bd)

    def insertar_producto(self, codigo, nombre, precio_lista, precio_c_iva, stock, proveedor):
        connexion = self.conectar()
        cursor = connexion.cursor()
        cursor.execute(
            "INSERT INTO Productos (codigo, nombre, precio_lista, precio_c_iva, precio_final, stock, proveedor) VALUES (?, ?, ?, ?, 0, ?, ?)",
            (codigo, nombre, precio_lista, precio_c_iva, stock, proveedor)
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
        cursor.execute("""
            UPDATE Productos
            SET codigo = ?, nombre = ?, precio_lista = ?, precio_c_iva = ?, stock = ?, proveedor = ?
            WHERE id = ?
        """, (codigo, nombre, precio_lista, precio_c_iva, stock, proveedor, id_producto))
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
        cursor = connexion.cursor()

        with open(ruta_csv, encoding="latin-1") as archivo:
            lector = csv.reader(archivo)
            empezar = False

            for fila in lector:
                if not empezar:
                    if len(fila) > 0 and fila[0].strip().upper() == "CODIGO":
                        empezar = True
                    continue

                if len(fila) < 5:
                    continue

                codigo = fila[0].strip()
                nombre = fila[1].strip()
                precio_lista = fila[2].replace(",", ".").strip()
                precio_c_iva = fila[4].replace(",", ".").strip()

                if not codigo or not precio_c_iva:
                    continue

                cursor.execute("SELECT id FROM Productos WHERE codigo = ? AND proveedor = ?", (codigo, "POL"))
                existe = cursor.fetchone()

                if existe:
                    cursor.execute("UPDATE Productos SET nombre = ?, precio_lista = ?, precio_c_iva = ? WHERE id = ?", (nombre, precio_lista, precio_c_iva, existe[0]))
                else:
                    cursor.execute("INSERT INTO Productos (codigo, nombre, precio_lista, precio_c_iva, precio_final, stock, proveedor) VALUES (?, ?, ?, ?, 0, 0, ?)", (codigo, nombre, precio_lista, precio_c_iva, "POL"))

        connexion.commit()
        connexion.close()
    def actualizar_precios_fgp(self, ruta_csv):
        connexion = self.conectar()
        cursor = connexion.cursor()

        with open(ruta_csv, encoding="latin-1") as archivo:
            lector = csv.reader(archivo)
            empezar = False

            for fila in lector:
                if not empezar:
                    if len(fila) > 0 and fila[0].strip().upper() == "CODIGO":
                        empezar = True
                    continue

                if len(fila) < 6:
                    continue

                codigo = fila[0].strip()
                nombre = fila[2].strip()
                precio_lista = fila[3].replace(",", ".").strip()
                precio_c_iva = fila[5].replace(",", ".").strip()

                if not codigo or not precio_c_iva:
                    continue

                cursor.execute("SELECT id FROM Productos WHERE codigo = ? AND proveedor = ?", (codigo, "FGP"))
                existe = cursor.fetchone()

                if existe:
                    cursor.execute("UPDATE Productos SET nombre = ?, precio_lista = ?, precio_c_iva = ? WHERE id = ?", (nombre, precio_lista, precio_c_iva, existe[0]))
                else:
                    cursor.execute("INSERT INTO Productos (codigo, nombre, precio_lista, precio_c_iva, precio_final, stock, proveedor) VALUES (?, ?, ?, ?, 0, 0, ?)", (codigo, nombre, precio_lista, precio_c_iva, "FGP"))

        connexion.commit()
        connexion.close()

    def actualizar_precios_day(self, ruta_csv):
        connexion = self.conectar()
        cursor = connexion.cursor()

        with open(ruta_csv, encoding="latin-1") as archivo:
            lector = csv.reader(archivo)
            empezar = False

            for fila in lector:
                if not empezar:
                    if len(fila) > 0 and fila[0].strip().upper() == "MARCA":
                        empezar = True
                    continue

                if len(fila) < 4:
                    continue

                nombre = fila[1].strip()
                precio = fila[3].replace(",", ".").strip()

                if not nombre or not precio:
                    continue

                cursor.execute("SELECT id FROM Productos WHERE nombre = ? AND proveedor = ?", (nombre, "DAY"))
                existe = cursor.fetchone()

                if existe:
                    cursor.execute("UPDATE Productos SET precio_lista = ?, precio_c_iva = ? WHERE id = ?", (precio, precio, existe[0]))
                else:
                    cursor.execute("INSERT INTO Productos (codigo, nombre, precio_lista, precio_c_iva, precio_final, stock, proveedor) VALUES (?, ?, ?, ?, 0, 0, ?)", ("", nombre, precio, precio, "DAY"))

        connexion.commit()
        connexion.close()

    def actualizar_precios_grays(self, ruta_csv):
        connexion = self.conectar()
        cursor = connexion.cursor()

        with open(ruta_csv, encoding="latin-1") as archivo:
            lector = csv.reader(archivo)
            empezar = False

            for fila in lector:
                if not empezar:
                    if len(fila) > 0 and fila[0].strip().upper() == "CODIGO FLEXXUS":
                        empezar = True
                    continue

                if len(fila) < 6:
                    continue

                codigo = fila[0].strip()
                nombre = fila[1].strip()
                precio = fila[5].replace(",", ".").strip()

                if not codigo or not precio:
                    continue

                cursor.execute("SELECT id FROM Productos WHERE codigo = ? AND proveedor = ?", (codigo, "GRAYS"))
                existe = cursor.fetchone()

                if existe:
                    cursor.execute("UPDATE Productos SET nombre = ?, precio_lista = ?, precio_c_iva = ? WHERE id = ?", (nombre, precio, precio, existe[0]))
                else:
                    cursor.execute("INSERT INTO Productos (codigo, nombre, precio_lista, precio_c_iva, precio_final, stock, proveedor) VALUES (?, ?, ?, ?, 0, 0, ?)", (codigo, nombre, precio, precio, "GRAYS"))

        connexion.commit()
        connexion.close()

    def aplicar_margen(self, proveedor, margen):
        connexion = self.conectar()
        cursor = connexion.cursor()
        cursor.execute("""
            UPDATE Productos
            SET precio_final = precio_c_iva * ?
            WHERE proveedor = ?
        """, (margen, proveedor))
        connexion.commit()
        connexion.close()