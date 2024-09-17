import pandas as pd
import os

# Directorios de origen
directorios = ["my_data_2021","my_data_2022", "my_data_2023_full", "my_data_2024_full"]

# Nombres de los archivos a combinar
archivos = ["customers_data", "customers_reservations", "reservations", "room_reservations"]

# Crear un diccionario para almacenar los DataFrames por tipo de archivo
dfs_por_tipo = {archivo: [] for archivo in archivos}

# Iterar sobre los directorios y archivos
for directorio in directorios:
    for archivo in archivos:
        ruta_completa = os.path.join(directorio, f"{archivo}.csv")
        df = pd.read_csv(ruta_completa)
        dfs_por_tipo[archivo].append(df)

# Concatenar los DataFrames por tipo de archivo
for archivo, lista_dfs in dfs_por_tipo.items():
    df_final = pd.concat(lista_dfs, ignore_index=True)
    df_final.to_csv(f"data/{archivo}.csv", index=False)