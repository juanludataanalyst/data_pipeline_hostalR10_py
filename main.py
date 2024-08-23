from api_calls import get_data_for_period, save_all_dataframes_to_csv,get_room_name_type,get_customer_info
import datetime
import pandas as pd
import os



# Example usage with more specific filtering
#created_start = datetime.date(2019, 2, 25)
created_start = datetime.date(2024, 8, 1)
created_end = datetime.date(2024, 8, 25)
arrival_start = datetime.date(2024, 8, 11)
arrival_end = datetime.date(2025, 12, 31)

dataframes_reservation_list = [] # List for reservations (Dictionaries)
start_date = created_start

while start_date <= created_end:
    # Calcular la fecha de fin del período 
    loop_date = start_date 
   
    # Asegurarse de que biweekly_end_date no exceda la fecha de fin general
    loop_date = min(loop_date, created_end)
    
    
    dataframes = get_data_for_period( start_date,  loop_date,arrival_start,arrival_end)
    
    if  dataframes:  #Add to list if api return something
        dataframes_reservation_list.append(dataframes)
    
    # Actualizar start_date para el siguiente período quincenal
    start_date = loop_date + datetime.timedelta(days=1)
    

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





os.makedirs("my_data", exist_ok=True) 
output_directory = "my_data"
#output_directory = "my_data"  # Cambia esto por la ruta de tu directorio de salida




reservations_df.to_csv(os.path.join(output_directory,"reservations.csv"),index=False, sep=',')
room_reservation_df.to_csv(os.path.join(output_directory,"room_reservations.csv"),index=False, sep=',')
customers_reservation_df.to_csv(os.path.join(output_directory,"customers_reservations.csv"),index=False, sep=',')
room_name_df.to_csv(os.path.join(output_directory,"room_name.csv"),index=False, sep=',')
customer_data_df.to_csv(os.path.join(output_directory,"customers_data.csv"),index=False, sep=',')



#save_all_dataframes_to_csv(dataframes_reservation_list,output_directory)
print("Fin del programa")
