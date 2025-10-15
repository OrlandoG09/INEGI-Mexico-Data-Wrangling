import pandas as pd 
from pathlib import Path
import glob 

# --- CONFIGURACIÓN ---
# Define la ruta donde se encuentran los reportes de porcentajes de residencia (*p.csv)
RUTA_REPORTES = Path(r'd:\Porcentajes de condicion de residencia 2014-2025')
PATRON_ARCHIVOS = '*.csv'
COLUMNA_VALOR = 'Porcentaje_Nuevo_Residente'
ENTIDADES_INTERES = ['CHIAPAS', 'TABASCO', 'QUINTANA ROO']
ARCHIVO_SALIDA = Path('Reporte_NR_Inflacion.csv')

def consolidar_reportes(ruta: Path, patron: str, columna: str, entidades: list) -> pd.DataFrame:
    """
    Recorre archivos CSV de reportes, calcula el promedio nacional y extrae valores específicos.
    """
    # Usar glob para encontrar todos los archivos que coinciden con el patrón
    patron_completo = str(ruta / patron)
    lista_archivos = glob.glob(patron_completo)
    
    if not lista_archivos:
        print(f" No se encontraron archivos en: {ruta} con el patrón {patron}.")
        return pd.DataFrame()

    print(f"Se encontraron {len(lista_archivos)} archivos de reporte para consolidar.")

    resultados = []

    for archivo in lista_archivos:
        try:
            df_t = pd.read_csv(archivo)
            
            # Cálculo del promedio nacional (Promedio simple, no ponderado en este script)
            promedio_nacional = df_t[columna].mean()
            
            datos_trimestre = {
                'Año/Trimestre': Path(archivo).name,
                f'Promedio_NR_Nacional': promedio_nacional
            }

            # Extracción de valores específicos por entidad
            for entidad in entidades:
                # Usar .loc de forma segura para obtener el valor
                valor_entidad = df_t.loc[df_t['Nombre_Entidad'] == entidad, columna]
                
                datos_trimestre[f'NR_{entidad.replace(" ", "_")}'] = valor_entidad.iloc[0] if not valor_entidad.empty else None
            
            resultados.append(datos_trimestre)
            print(f" Procesado: {Path(archivo).name}")
            
        except Exception as e:
            print(f" Error al procesar {Path(archivo).name}: {e}")

    df_final = pd.DataFrame(resultados)
    return df_final.sort_values(by='Año/Trimestre')

def main_promedios():
    df_consolidado = consolidar_reportes(RUTA_REPORTES, PATRON_ARCHIVOS, COLUMNA_VALOR, ENTIDADES_INTERES)

    if not df_consolidado.empty:
        print("\n--- Reporte Consolidado de Nuevo Residente (NR) ---")
        print(df_consolidado.round(4))
        
        df_consolidado.to_csv(ARCHIVO_SALIDA, index=False)
        print(f"\n Archivo guardado: {ARCHIVO_SALIDA}")

if __name__ == '__main__':
    main_promedios()