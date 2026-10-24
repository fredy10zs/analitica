# analitica

paso 1
comando 

python -m venv .venv

paso 2 activar el entorno

source  .venv/bin/activate

 Actividad: Procesamiento de archivos CSV y JSON

 Fuentes de datos

- **CSV — Fast Food Restaurants:** [Descargar archivo CSV](https://huggingface.co/datasets/JasonZhouTI/Fast_Food_Restaurants/resolve/main/FastFoodRestaurants.csv?download=true)
- **JSON — Country Capitals:** [Consultar countries.json](https://huggingface.co/datasets/false-facts-finetuning/country-capitals/blob/main/countries.json)

Los archivos originales se conservan separados de las copias modificadas.

Estructura de archivos

- `Actividad_CSV_JSON.ipynb`: coordina el procesamiento y muestra los resultados.
- `datos_csv_json/FastFoodRestaurants.csv`: CSV original.
- `datos_csv_json/FastFoodRestaurants_modificado.csv`: CSV transformado.
- `datos_csv_json/countries.json`: JSON original.
- `datos_csv_json/countries_modificado.json`: JSON transformado.
- `clases_po/manejador_csv.py`: clase `ManejadorCSV`.
- `clases_po/manejador_json.py`: clase `ManejadorJSON`.
- `clases_po/generador_resumen_txt.py`: clase `GeneradorResumenTXT`.
- `reportes/resumen_csv_json.txt`: resumen del procesamiento.

Transformaciones realizadas

CSV

La clase `ManejadorCSV` importa los datos mediante `csv.reader`, modifica el nombre del primer restaurante añadiendo `- Revisado` y guarda una copia mediante `csv.writer`.

Json

La clase `ManejadorJSON` importa los datos con `json.load`, modifica el campo `display_name` del primer país y guarda una copia con `json.dump`.

Resumen txt

La clase `GeneradorResumenTXT` genera un informe con las URL de origen, los archivos procesados, los cambios realizados, las rutas de salida, las cantidades de registros y los métodos utilizados.

## Resultados comprobados

- CSV: 10.000 registros.
- JSON: 194 países.

Las rutas del notebook están configuradas para ejecutarse desde `src/sincronicas/`.
