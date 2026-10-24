
class GeneradorResumenTXT:
    def __init__(self, url_csv, url_json, resultado_csv, resultado_json):
        self.url_csv = url_csv
        self.url_json = url_json
        self.resultado_csv = resultado_csv
        self.resultado_json = resultado_json

    def generar(self, ruta_destino):
        lineas = [
            "Resumen del procesamiento cvs y json",
            "=" * 45,
            "",
            f"URL de origen del CSV: {self.url_csv}",
            f"URL de origen del JSON: {self.url_json}",
            "",
            "Procesamiento csv",
            "-" * 25,
            f"Archivo importado: {self.resultado_csv['archivo_origen']}",
            f"Modificación: {self.resultado_csv['modificacion']}",
            f"Archivo guardado: {self.resultado_csv['archivo_salida']}",
            f"Registros procesados: {self.resultado_csv['registros']}",
            f"Clase utilizada: {self.resultado_csv['clase']}",
            f"Métodos utilizados: {self.resultado_csv['metodos']}",
            "",
            "Procesamiento json",
            "-" * 25,
            f"Archivo importado: {self.resultado_json['archivo_origen']}",
            f"Modificación: {self.resultado_json['modificacion']}",
            f"Archivo guardado: {self.resultado_json['archivo_salida']}",
            f"Registros procesados: {self.resultado_json['registros']}",
            f"Clase utilizada: {self.resultado_json['clase']}",
            f"Métodos utilizados: {self.resultado_json['metodos']}",
            "",
        ]

        with open(ruta_destino, mode="w", encoding="utf-8") as archivo:
            archivo.write("\n".join(lineas))

        return ruta_destino
