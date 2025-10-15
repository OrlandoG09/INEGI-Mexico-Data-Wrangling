import pandas as pd

# --- CONFIGURACIÓN ---
ARCHIVO_ENTRADA = "Trimestre 2 de 2020m.csv" # Archivo resultante de la concatenación
NOMBRE_ARCHIVO_SALIDA = "Trimestre_2_2020p.csv"
COLUMNAS_RENOMBRAR = {
    'MUN,C,3': 'Municipio',
    'ENT,C,2': 'Entidad_Clave', # Cambiado a "Clave" para diferenciarlo del nombre
    'C_RES,C,1': 'Condicion_Residencia',
    'L_NAC_C,C,3': 'Lugar_Residencia',
    # Usar el nombre del nuevo factor ajustado
    'FAC_T2_2020_AJUSTADO':'Factor_Expansion' 
}
MAPA_ENTIDADES = {
    1: 'AGUASCALIENTES', 2: 'BAJA CALIFORNIA', 3: 'BAJA CALIFORNIA SUR', 4: 'CAMPECHE',
    5: 'COAHUILA DE ZARAGOZA', 6: 'COLIMA', 7: 'CHIAPAS', 8: 'CHIHUAHUA',
    9: 'CIUDAD DE MEXICO', 10: 'DURANGO', 11: 'GUANAJUATO', 12: 'GUERRERO', 13: 'HIDALGO',
    14: 'JALISCO', 15: 'MEXICO', 16: 'MICHOACAN DE OCAMPO', 17: 'MORELOS',
    18: 'NAYARIT', 19: 'NUEVO LEON', 20: 'OAXACA', 21: 'PUEBLA',
    22: 'QUERETARO DE ARTEAGA', 23: 'QUINTANA ROO', 24: 'SAN LUIS POTOSI',
    25: 'SINALOA', 26: 'SONORA', 27: 'TABASCO', 28: 'TAMAULIPAS',
    29: 'TLAXCALA', 30: 'VERACRUZ DE IGNACIO DE LA LLAVE', 31: 'YUCATAN',
    32: 'ZACATECAS'
}
COLUMNA_CLAVE_ENTIDAD = 'Entidad_Clave'
COLUMNA_CONDICION_RESIDENCIA = 'Condicion_Residencia'
COLUMNA_FACTOR = 'Factor_Expansion'

def cargar_y_limpiar_datos(archivo: str, renombrar: dict) -> pd.DataFrame:
    """Carga, renombra y convierte a numérico las columnas clave."""
    try:
        df = pd.read_csv(archivo, encoding='latin1')
    except FileNotFoundError:
        print(f"Error: Asegúrate de que el archivo '{archivo}' esté en la misma carpeta.")
        return pd.DataFrame()

    df.rename(columns=renombrar, inplace=True)
    
    # Limpieza de datos
    df[COLUMNA_CONDICION_RESIDENCIA] = pd.to_numeric(df[COLUMNA_CONDICION_RESIDENCIA], errors='coerce').fillna(0).astype(int)
    df[COLUMNA_FACTOR] = pd.to_numeric(df[COLUMNA_FACTOR], errors='coerce').fillna(0)
    
    # Filtrar solo valores válidos para Condición de Residencia (1, 2, 3)
    df = df[df[COLUMNA_CONDICION_RESIDENCIA].isin([1, 2, 3])].copy()
    
    return df

def calcular_porcentajes_residencia(df: pd.DataFrame, mapa_entidades: dict) -> pd.DataFrame:
    """Calcula la tabla pivote de porcentajes de condición de residencia por entidad."""
    
    # 1. Mapear claves a nombres de entidad
    df['Nombre_Entidad'] = df[COLUMNA_CLAVE_ENTIDAD].map(mapa_entidades)

    # 2. Crear tabla pivote con la población absoluta (suma del Factor_Expansion)
    tabla_absoluta = df.pivot_table(
        index='Nombre_Entidad',
        columns=COLUMNA_CONDICION_RESIDENCIA,
        values=COLUMNA_FACTOR,
        aggfunc='sum',
        fill_value=0
    )

    # 3. Calcular el total de población por entidad y los porcentajes
    tabla_absoluta['Poblacion_Total'] = tabla_absoluta.sum(axis=1)
    tabla_porcentajes = pd.DataFrame(index=tabla_absoluta.index) 

    # Diccionario para mapear códigos a nombres descriptivos de columnas
    mapeo_columnas = {
        1: 'Porcentaje_Residente_Habitual', 
        2: 'Porcentaje_Ausente_Definitivo', 
        3: 'Porcentaje_Nuevo_Residente'
    }

    for codigo, nombre_columna in mapeo_columnas.items():
        if codigo in tabla_absoluta.columns:
            tabla_porcentajes[nombre_columna] = (tabla_absoluta[codigo] / tabla_absoluta['Poblacion_Total']) * 100
        else:
            tabla_porcentajes[nombre_columna] = 0.0 # Asegura que la columna exista

    # Añadir columna de verificación
    tabla_porcentajes['Suma_Verificacion'] = tabla_porcentajes.iloc[:, :3].sum(axis=1).round(5) 
    
    return tabla_porcentajes

def main_residencia():
    df_procesado = cargar_y_limpiar_datos(ARCHIVO_ENTRADA, COLUMNAS_RENOMBRAR)
    
    if not df_procesado.empty:
        tabla_final = calcular_porcentajes_residencia(df_procesado, MAPA_ENTIDADES)
        
        print("\n--- Tabla Final con Porcentajes por Entidad ---")
        print(tabla_final.round(2)) 
        
        tabla_final.to_csv(NOMBRE_ARCHIVO_SALIDA)
        print(f"\n Tabla de porcentajes guardada en '{NOMBRE_ARCHIVO_SALIDA}'")

if __name__ == '__main__':
    main_residencia()