# INEGI-Data-Wrangler: Automatización para Análisis Económico de México

Scripts de Python para el preprocesamiento, limpieza y cálculo de indicadores socioeconómicos a partir de microdatos brutos del **INEGI**, específicamente de la **ENOE** (Encuesta Nacional de Ocupación y Empleo) y el **INPC** (Índice Nacional de Precios al Consumidor).

El objetivo es transformar los archivos originales en bases de datos analíticas, permitiendo el cálculo de indicadores geográficos y series de tiempo (como la inflación).

## Características Principales

Este proyecto automatiza tareas clave para el análisis de datos mexicanos:

1.  **Limpieza de Microdatos ENOE:** Filtra bases `.xls`/`.xlsx` para obtener únicamente variables esenciales (Entidad, Municipio, Condición de Residencia y Factor de Expansión).
2.  **Agregación Trimestral y Ponderación:** Combina los archivos mensuales de la ENOE y ajusta el Factor de Expansión dividiéndolo entre tres para obtener el ponderador trimestral correcto.
3.  **Cálculo de Indicadores Sociales:** Genera reportes del **Porcentaje de Condición de Residencia** (Residente Habitual, Nuevo Residente, Ausente Definitivo) por Entidad Federativa, utilizando la expansión poblacional.
4.  **Cálculo de Inflación:** Utiliza los datos del INPC para calcular la **Inflación Trimestral Discreta** (variación porcentual en 3 meses).
5.  **Consolidación de Reportes:** Genera tablas finales que consolidan métricas clave (ej. promedio nacional de "Nuevo Residente" vs. estados de interés) a lo largo del tiempo.

##  Estructura y Scripts

El repositorio se compone de los siguientes scripts principales, ordenados por su función en el *pipeline*:

| Nombre del Script | Propósito | Salida de Muestra |
| :--- | :--- | :--- |
| **`Filtrar atributos requeridos.py`** | Filtra columnas esenciales de archivos mensuales ENOE. | `juniom.csv` |
| **`Concatener bases de datos mensuales.py`** | Une bases mensuales y ajusta el Factor de Expansión a nivel trimestral. | `Trimestre 2 de 2020m.csv` |
| **`Porcentaje de condicion de residencia*.py`** | Calcula la distribución porcentual de la Condición de Residencia por Entidad. | `reporte_porcentajes_residencia.csv` |
| **`Calcular inflacion nacional.py`** | Calcula la inflación trimestral usando el INPC. | `InflacionTuxtla.csv` |
| **`Promedios_inflacion.py`** | Consolidación y resumen de métricas (ej. Promedio Nacional vs. Chiapas, Tabasco, QRoo). | `Reporte_NR_Inflacion.csv` |

## Uso e Implementación

### 1. Requisitos

Asegúrate de tener instaladas las siguientes librerías de Python:

### bash
pip install pandas numpy openpyxl
