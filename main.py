from api_calls import get_data_for_period, save_all_dataframes_to_csv,get_room_name_type
import datetime
import pandas as pd



# Example usage with more specific filtering
created_start = datetime.date(2024, 8, 19)
created_end = datetime.date(2024, 8, 20)
arrival_start = datetime.date(2024, 8, 19)
arrival_end = datetime.date(2024, 12, 31)


dataframes_reservation_list = []
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
    
room_info_df = pd.DataFrame(get_room_name_type())


output_directory = "data_pruebas"  # Cambia esto por la ruta de tu directorio de salida
save_all_dataframes_to_csv(dataframes_reservation_list,output_directory)

