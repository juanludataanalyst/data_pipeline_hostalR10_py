from api_calls import get_and_save_all_dataframes
import time



# Timestamp al inicio del programa
inicio = time.time()
print(f"Inicio del programa: {inicio}")


get_and_save_all_dataframes()

# Timestamp al final del programa
fin = time.time()
print(f"Fin del programa: {fin}")

# Puedes calcular también el tiempo de ejecución
tiempo_ejecucion = fin - inicio
print(f"Tiempo de ejecución: {tiempo_ejecucion} segundos")




