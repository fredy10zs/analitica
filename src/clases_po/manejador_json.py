
import json


class ManejadorJSON:
    def __init__(self, ruta_origen):
        self.ruta_origen = ruta_origen
        self.datos = None
        self.modificacion = ""
        self.ruta_salida = ""

    def importar(self):
        with open(self.ruta_origen, mode="r", encoding="utf-8") as archivo:
            self.datos = json.load(archivo)

        return self.datos


    def modificar(self):
        if self.datos is None:
            raise ValueError(" se debe importar el archivo json.")

        if not isinstance(self.datos, list) or not self.datos:
            raise ValueError(
                "El json debe contener una lista."
            )

        primer_pais = self.datos[0]

        if not isinstance(primer_pais, dict):
            raise ValueError("El primer elemento no es un objeto json.")

        if "display_name" not in primer_pais:
            raise ValueError(
                "El primer país no contiene el campo 'display_name'."
            )

        nombre_original = primer_pais["display_name"]
        primer_pais["display_name"] = nombre_original + " - Revisado"

        self.modificacion = (
            f"Se modificó display_name del primer país: "
            f"'{nombre_original}' -> "
            f"'{primer_pais['display_name']}'."
        )

        return self.datos


    def guardar(self, ruta_destino):
        with open(ruta_destino, mode="w", encoding="utf-8") as archivo:
            json.dump(self.datos, archivo, ensure_ascii=False, indent=4)

        self.ruta_salida = ruta_destino
        return ruta_destino
