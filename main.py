from api_calls import get_data_for_period, save_all_dataframes_to_csv,get_room_name_type,get_customer_info,get_reservations_df
import datetime
import pandas as pd
import os

#created_start = datetime.date(2019, 2, 25)
created_start = datetime.date(2024, 1, 1)
created_end = datetime.date(2024, 1, 2)
arrival_start = datetime.date(2024, 2, 1)
arrival_end = datetime.date(2025, 12, 31)

dataframes_reservation_list = get_reservations_df(created_start, created_end, arrival_start, arrival_end)
  
room_name_df = pd.DataFrame(get_room_name_type())

 # Getting customer_ids and calling api for getting information
all_customer_ids = []

for df in dataframes_reservation_list:
    if not df['customers'].empty:
        customer_ids = df['customers']['id_customer'].tolist()
        all_customer_ids.extend(customer_ids)

all_customer_ids = list(set(all_customer_ids))

customer_data = [get_customer_info(customer_id) for customer_id in all_customer_ids ]

customer_data_df = pd.DataFrame(customer_data)


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
