import numpy as np
import pandas as pd 
from pathlib import Path

# --- CONFIGURACIÓN ---
ARCHIVO_ENTRADA = 'INPC_SOLOS.csv'
COLUMNA_INPC = 'INPC TUXTLA' # Columna del INPC a utilizar (¡Asegúrate que sea la correcta!)
MESES_PERIODO = 3 # Cálculo trimestral (3 meses)
NOMBRE_COLUMNA_SALIDA = 'Inflacion_TRIMESTRAL_FINAL'
ARCHIVO_SALIDA = Path('InflacionTuxtla.csv')

def calcular_inflacion_trimestral(df: pd.DataFrame, inpc_col: str, periodo: int) -> pd.DataFrame:
    """
    Calcula la variación porcentual discreta (inflación) para un periodo dado.
    Marca el resultado solo en el último mes del periodo.
    """
    if inpc_col not in df.columns:
        raise KeyError(f"La columna '{inpc_col}' no se encuentra en el DataFrame.")
        
    df = df.copy() # Trabajar en una copia para evitar SettingWithCopyWarning
    
    # INPC del mes inicial del periodo (ej. 3 meses atrás si periodo=3)
    df[f'INPC_Mes_Inicio'] = df[inpc_col].shift(periodo - 1)

    # Inflacion: (INPC_Actual - INPC_Inicio) / INPC_Inicio * 100
    df['Inflacion_Pct'] = (
        (df[inpc_col] - df[f'INPC_Mes_Inicio']) / df[f'INPC_Mes_Inicio']
    ) * 100

    # Filtrar y dejar solo los resultados al final de cada periodo
    df[NOMBRE_COLUMNA_SALIDA] = np.where(
        (df.index + 1) % periodo == 0,
        df['Inflacion_Pct'],
        np.nan 
    )
    
    return df

def main_inflacion():
    try:
        df = pd.read_csv(ARCHIVO_ENTRADA)
    except FileNotFoundError:
        print(f" Error: Archivo de entrada '{ARCHIVO_ENTRADA}' no encontrado.")
        return

    try:
        df_calculado = calcular_inflacion_trimestral(df, COLUMNA_INPC, MESES_PERIODO)
        
        # Extraer solo la serie limpia de resultados
        serie_inflacion_limpia = df_calculado[NOMBRE_COLUMNA_SALIDA].dropna()
        
        print("\n--- Resultado del Cálculo Trimestral Discreto ---")
        print(serie_inflacion_limpia)

        # Guardar la serie de resultados
        serie_inflacion_limpia.to_csv(ARCHIVO_SALIDA, index=True, header=[NOMBRE_COLUMNA_SALIDA])
        print(f"\n Archivo guardado: {ARCHIVO_SALIDA}")
        
    except KeyError as e:
        print(f" Error en el cálculo: {e}")

if __name__ == '__main__':
    main_inflacion()