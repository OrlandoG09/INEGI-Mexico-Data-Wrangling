import pandas as pd
from pathlib import Path

# --- CONFIGURACIÓN ---
# Define la carpeta de entrada y el archivo a procesar
ARCHIVO_ENTRADA = "junio.xls"

# Columnas originales de la ENOE que queremos conservar
COLUMNAS_REQUERIDAS = [
    'MUN,C,3',      # Municipio
    'ENT,C,2',      # Entidad
    'C_RES,C,1',    # Condición de residencia
    'L_NAC_C,C,3',  # Lugar de residencia
    'FAC_NP,N,6,0'  # Factor de expansión mensual
]
# Sufijo para el archivo de salida
SUFIJO_SALIDA = 'm.csv'

def filtrar_y_guardar(archivo_entrada: str, columnas: list):
    """
    Carga un archivo de microdatos de la ENOE, filtra las columnas requeridas
    y guarda el resultado en un archivo CSV.
    """
    ruta_entrada = Path(archivo_entrada)
    nombre_base = ruta_entrada.stem
    ruta_salida = ruta_entrada.with_name(f'{nombre_base}{SUFIJO_SALIDA}')
    
    print(f"Iniciando carga y filtrado del archivo: {archivo_entrada}")
    
    try:
        # Cargar el archivo, asumiendo Excel/xls/xlsx
        df_completo = pd.read_excel(ruta_entrada)

        # Filtrar el DataFrame
        df_filtrado = df_completo[columnas]

        # Guardar el resultado en un nuevo archivo CSV
        df_filtrado.to_csv(ruta_salida, index=False)
        
        print(f" ¡Éxito! Archivo guardado en '{ruta_salida.name}' con las columnas filtradas.")

    except FileNotFoundError:
        print(f" Error: No se encontró el archivo '{archivo_entrada}' en la ubicación actual.")
    except KeyError as e:
        print(f" Error: La columna {e} no se encontró en el archivo. Verifique nombres en COLUMNAS_REQUERIDAS.")
    except Exception as e:
        print(f" Ocurrió un error inesperado: {e}")

if __name__ == '__main__':
    # Para procesar varios meses, podrías convertir ARCHIVO_ENTRADA en una lista
    # y llamar a la función en un bucle.
    filtrar_y_guardar(ARCHIVO_ENTRADA, COLUMNAS_REQUERIDAS)
    
    