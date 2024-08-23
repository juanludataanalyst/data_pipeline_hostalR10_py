from api_calls import get_customer_data_df, save_all_dataframes_to_csv,get_room_name_type,get_reservations_df_list
import datetime
import pandas as pd
import os

#created_start = datetime.date(2019, 2, 25)
created_start = datetime.date(2024, 1, 1)
created_end = datetime.date(2024, 1, 2)
arrival_start = datetime.date(2024, 2, 1)
arrival_end = datetime.date(2025, 12, 31)

dataframes_reservation_list = get_reservations_df_list(created_start, created_end, arrival_start, arrival_end)
  
room_name_df = get_room_name_type()

customer_data_df = get_customer_data_df(dataframes_reservation_list)

# Crear listas vacías para almacenar los DataFrames combinados
reservations_list, room_reservation_list, customers_reservation_list = [], [], []

for diccionario in dataframes_reservation_list:
    reservations_list.append(diccionario['reservations'])
    room_reservation_list.append(diccionario['room_reservas'])
    customers_reservation_list.append(diccionario['customers'])

reservations_df = pd.concat(reservations_list, ignore_index=True)
room_reservation_df = pd.concat(room_reservation_list, ignore_index=True)
customers_reservation_df = pd.concat(customers_reservation_list, ignore_index=True) 





os.makedirs("my_data_2024", exist_ok=True) 
output_directory = "my_data_2024"
#output_directory = "my_data"  # Cambia esto por la ruta de tu directorio de salida




reservations_df.to_csv(os.path.join(output_directory,"reservations.csv"),index=False, sep=',')
room_reservation_df.to_csv(os.path.join(output_directory,"room_reservations.csv"),index=False, sep=',')
customers_reservation_df.to_csv(os.path.join(output_directory,"customers_reservations.csv"),index=False, sep=',')
room_name_df.to_csv(os.path.join(output_directory,"room_name.csv"),index=False, sep=',')
customer_data_df.to_csv(os.path.join(output_directory,"customers_data.csv"),index=False, sep=',')



#save_all_dataframes_to_csv(dataframes_reservation_list,output_directory)
print("Fin del programa")
