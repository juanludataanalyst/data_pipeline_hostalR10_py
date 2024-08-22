from api_calls import get_data_for_period, save_all_dataframes_to_csv,get_room_name_type,get_customer_info
import datetime
import pandas as pd



# Example usage with more specific filtering
created_start = datetime.date(2024, 8, 20)
created_end = datetime.date(2024, 8, 20)
arrival_start = datetime.date(2024, 8, 19)
arrival_end = datetime.date(2024, 12, 31)

dataframes_reservation_list = [] # List for reservations (Dictionaries)
start_date = created_start

while start_date <= created_end:
    # Calcular la fecha de fin del período 
    loop_date = start_date 
   
    # Asegurarse de que biweekly_end_date no exceda la fecha de fin general
    loop_date = min(loop_date, created_end)
    
    
    dataframes = get_data_for_period( start_date,  loop_date,arrival_start,arrival_end)
    
    print(dataframes)    
    dataframes_reservation_list.append(dataframes)
    
    # Actualizar start_date para el siguiente período quincenal
    start_date = loop_date + datetime.timedelta(days=1)
    
room_info_df_dict = {"name_type":pd.DataFrame(get_room_name_type())}

 # Getting customer_ids and calling api for getting information
all_customer_ids = []
for df in dataframes_reservation_list:
    customer_ids = df['customers']['id_customer'].tolist()
    all_customer_ids.extend(customer_ids)

all_customer_ids = list(set(all_customer_ids))

customer_data = [get_customer_info(customer_id) for customer_id in all_customer_ids ]

customer_data_info_df_dict =  {"customer_data":pd.DataFrame(customer_data)}



dataframes_reservation_list .append(customer_data_info_df_dict)
dataframes_reservation_list .append(room_info_df_dict)


print("Aqui se imprime el dataframe list")
print("\n\n\n")
print("\n\n\n")
print(dataframes_reservation_list)
print("\n\n\n")
print("\n\n\n")


output_directory = "data_pruebas"  # Cambia esto por la ruta de tu directorio de salida
save_all_dataframes_to_csv(dataframes_reservation_list,output_directory)

