import os

def save_dataframes_to_csv(dataframes, output_dir):
    """
    Guarda múltiples DataFrames en archivos CSV separados.

    Args:
        dataframes: Un diccionario donde las claves son los nombres de los DataFrames y los valores son los DataFrames.
        output_dir: La ruta al directorio donde se guardarán los archivos.
    """

    for df_name, df in dataframes.items():
        file_path = os.path.join(output_dir, f"{df_name}.csv")
        df.to_csv(file_path, index=False)

#