# Actividad 2.1 — Estandarización de pipelines y control de calidad de datos

Universidad Santo Tomás — Especialización en Ciencia de Datos — Seminario de Grado II.

## Objetivo
Automatizar la preparación, validación, entrenamiento y evaluación de un clasificador de especies Iris mediante un único comando, incorporando trazabilidad y controles de calidad.

## Arquitectura
```text
run_pipeline.py
  -> src/prepare.py
  -> src/validate_data.py
  -> src/train.py
  -> tests/test_model.py
```
El orquestador crea los directorios de trabajo y detiene la ejecución si cualquier etapa retorna un código distinto de cero (fail-fast).

## Instalación y reproducción
Se utilizó Google Colab con Python 3.13.18. Desde la raíz del repositorio, con Python instalado:
```sh
python -m venv .venv
```
Activar el entorno: `source .venv/bin/activate` (Linux/macOS) o `.venv\Scripts\activate` (Windows).
```sh
python -m pip install -r requirements.txt
python run_pipeline.py
```
Los datos y modelos se generan localmente; no es necesario descargarlos. Las dependencias directas están fijadas; las transitivas no están completamente bloqueadas.

## Datos y metodología
Iris de scikit-learn: 150 observaciones, cuatro medidas en centímetros y tres clases (0: setosa, 1: versicolor, 2: virginica). Partición estratificada 80/20 (120/30), semilla 42. Random Forest con 100 árboles, profundidad sin límite y semilla 42. Los identificadores se excluyen de los predictores y permiten comprobar que las particiones no comparten observaciones.

## Contrato de datos
| Variable | Tipo | Mínimo | Máximo |
|---|---|---:|---:|
| sepal_length | Número | 4 | 8 |
| sepal_width | Número | 2 | 4.5 |
| petal_length | Número | 1 | 7 |
| petal_width | Número | 0.1 | 2.5 |

Todas son obligatorias, finitas y no admiten nulos. Los rangos son decisiones del ejercicio, no límites biológicos universales. `data_contract.json` incluye ejemplos válidos e inválidos de inferencia. Los CSV incorporan además `species` y `row_id`. La validación utiliza exclusivamente la biblioteca estándar de Python y comprueba encabezados, tipos, nulos, rangos, clases, tamaños e identificadores.

## Trazabilidad
MLflow registra hiperparámetros, semillas, métricas, versión de Python, huellas SHA-256 de los datos, modelo, contrato y dependencias. Para consultar una ejecución local:
```sh
mlflow ui --backend-store-uri sqlite:///mlflow.db
```
Abrir http://127.0.0.1:5000. La base de datos y los artefactos se regeneran al ejecutar; no se incluyen en el repositorio.

## Resultados de la ejecución original en Colab
| Métrica | Resultado |
|---|---:|
| Accuracy de entrenamiento | 1.0000 |
| Accuracy de prueba | 0.9000 |
| F1 macro | 0.8997 |
| Umbral mínimo de accuracy | 0.8000 |

Run ID: `5661f9c48f294bacb83d2b13be973772`.

Se clasificaron correctamente 27 de 30 observaciones. La brecha de diez puntos porcentuales entre entrenamiento y prueba sugiere examinar la generalización, pero no demuestra por sí sola sobreajuste. El objetivo de esta actividad es el control de calidad y la automatización, no maximizar la métrica.

## Pruebas automatizadas y prueba negativa
```sh
python -m pytest -q tests
```
Las diez pruebas cubren entradas válidas e inválidas, nulos, rangos, tipos, ambos conjuntos, ausencia de IDs compartidos, número de variables del modelo y accuracy mínimo.

Para reproducir el fallo controlado después de una ejecución exitosa, desde la raíz:
```python
from pathlib import Path
p = Path("data/train.csv")
lines = p.read_text().splitlines()
row = lines[1].split(",")
row[0] = "cinco"
lines[1] = ",".join(row)
p.write_text("\n".join(lines) + "\n")
```
Ejecutar `python run_pipeline.py --sin-preparar`. Debe detenerse en Validar con código distinto de cero. Restaurar los datos con `python run_pipeline.py`.

## Evidencias y limitaciones
`reports/metrics.json`, `reports/pipeline.log` y `reports/negative_test.log` conservan los archivos originales de Colab. El log positivo exportado es parcial; para obtener un registro completo de una nueva ejecución puede usarse `python run_pipeline.py > reports/pipeline.log 2>&1` una vez exista el directorio reports. Las métricas pueden variar con el entorno. La comprobación de IDs no descarta todas las formas de fuga de datos. No cargar modelos pickle de fuentes no confiables.

## Fuentes y transparencia
- Libro Seminario de Grado II, apartado 2.7.
- Ruta de aprendizaje S2, actividad 2.1.
- Presentaciones de las sesiones 2 y 4.
- Código base de la actividad 1.1.

ChatGPT asistió en la generación y revisión del código, documentación e interpretación inicial. La estudiante ejecutó el notebook en Colab. La declaración definitiva debe reflejar la revisión y contribución efectivas de la estudiante.
