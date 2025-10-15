import pandas as pd
from pathlib import Path
import numpy as np


# Define la carpeta donde se encuentran los archivos filtrados (*m.csv)
RUTA_BASE = Path(r'd:\Bases de datos ENOE por trimestre DE 2014-2025\2020trim2') 
ARCHIVOS_MENSUALES = [
    'abrilm.csv',
    'mayom.csv',
    'juniom.csv'
]
VARIABLE_FACTOR_EXPANSION = 'FAC_NP,N,6,0'
NOMBRE_NUEVO_FACTOR = 'FAC_T2_2020_AJUSTADO'
VALOR_TRIMESTRE = '2020 T2'
NOMBRE_ARCHIVO_SALIDA = f"Trimestre_{VALOR_TRIMESTRE.replace(' ', '_')}.csv"

def ajustar_factor_expansion(df: pd.DataFrame, factor_col: str, nuevo_col: str, divisor: int) -> pd.DataFrame:
    """Ajusta el factor de expansión mensual dividiéndolo por el divisor (generalmente 3)."""
    if factor_col not in df.columns:
        raise KeyError(f"La columna '{factor_col}' no se encuentra en el DataFrame.")
    
    # Aplicar el ajuste crucial del factor
    df[nuevo_col] = pd.to_numeric(df[factor_col], errors='coerce') / divisor
    return df

def concatenar_y_ajustar_bases(ruta_base: Path, archivos: list):
    """
    Carga, ajusta el factor de expansión y concatena los archivos mensuales de la ENOE.
    """
    dataframes_list = []
    columnas_esenciales = [
        'MUN,C,3', 
        'ENT,C,2', 
        'C_RES,C,1',
        'L_NAC_C,C,3', 
        NOMBRE_NUEVO_FACTOR, # El nuevo ponderador
        'TRIMESTRE'
    ]

    print("Iniciando carga, ajuste y concatenación de datos...")

    for archivo in archivos:
        ruta_completa = ruta_base / archivo
        
        try:
            df_mes = pd.read_csv(ruta_completa, low_memory=False)
            
            # Crear variable de identificación de mes/trimestre
            df_mes['TRIMESTRE'] = VALOR_TRIMESTRE
            
            # Ajustar el factor de expansión
            df_mes = ajustar_factor_expansion(df_mes, VARIABLE_FACTOR_EXPANSION, NOMBRE_NUEVO_FACTOR, divisor=len(archivos))
            
            # Filtrar a las columnas esenciales
            df_mes = df_mes.filter(items=columnas_esenciales, axis=1)
            
            dataframes_list.append(df_mes)
            print(f" Archivo {archivo} procesado y ajustado.")
            
        except FileNotFoundError:
            print(f" Error: Archivo no encontrado en {ruta_completa}.")
        except Exception as e:
            print(f" Ocurrió un error al procesar {archivo}: {e}")

    # Unir todos los DataFrames y guardar
    if dataframes_list:
        df_final = pd.concat(dataframes_list, ignore_index=True)
        print(f"\n Concatenación completada. Total de observaciones: {len(df_final)}")
        
        ruta_salida = ruta_base / NOMBRE_ARCHIVO_SALIDA
        df_final.to_csv(ruta_salida, index=False)
        print(f" Archivo de salida guardado en: {ruta_salida}")
    else:
        print("\n No se pudo cargar ningún archivo. Revise las rutas y nombres.")

if __name__ == '__main__':
    concatenar_y_ajustar_bases(RUTA_BASE, ARCHIVOS_MENSUALES)
    