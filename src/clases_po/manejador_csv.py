
import csv


class ManejadorCSV:
    def __init__(self, ruta_origen):
        self.ruta_origen = ruta_origen
        self.datos = []
        self.encabezados = []
        self.modificacion = ""
        self.ruta_salida = ""

    def importar(self):
        with open(self.ruta_origen, mode="r", encoding="utf-8", newline="") as archivo:
            lector = csv.reader(archivo)
            filas = list(lector)

        if not filas:
            raise ValueError("El archivo CSV está vacío.")

        self.encabezados = filas[0]
        self.datos = filas[1:]
        return self.datos

    def modificar(self):
        if not self.datos:
            raise ValueError("Primero debes importar el archivo CSV.")

        # Cambia el nombre del primer restaurante para demostrar la modificación.
        indice_nombre = self.encabezados.index("name")
        nombre_original = self.datos[0][indice_nombre]
        self.datos[0][indice_nombre] = nombre_original + " - Revisado"

        self.modificacion = (
            f"Se modificó el nombre del primer registro: "
            f"'{nombre_original}' -> '{self.datos[0][indice_nombre]}'."
        )
        return self.datos

    def guardar(self, ruta_destino):
        with open(ruta_destino, mode="w", encoding="utf-8", newline="") as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(self.encabezados)
            escritor.writerows(self.datos)

        self.ruta_salida = ruta_destino
        return ruta_destino
