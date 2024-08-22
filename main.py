from api_calls import get_reservations_data, get_room_name_type, get_customer_info
import pandas as pd
import datetime
import os

def get_data_for_period(created_start, created_end, arrival_start, arrival_end):
  """
  Makes an API call within a specified date range for the created and arrival fields,
  and returns the dataframes.

  Args:
      created_start (datetime.datetime): Start date of the range for the created field.
      created_end (datetime.datetime): End date of the range for the created field.
      arrival_start (datetime.datetime): Start date of the range for the arrival field.
      arrival_end (datetime.datetime): End date of the range for the arrival field.

  Returns:
      dict: Dictionary with the four dataframes: reservations, room_reservas, customers, customer_data_info.
  """

  # Set filter parameters for the given period
  created = {'from': created_start.strftime('%d/%m/%Y'), 'to': created_end.strftime('%d/%m/%Y')}
  arrival = {'from': arrival_start.strftime('%d/%m/%Y'), 'to': arrival_end.strftime('%d/%m/%Y')}

  # Calling apis for reservations and room names
  reservations_data = get_reservations_data(created, arrival)
  room_info = get_room_name_type()

  # Converting raw data to dataframes
  reservations_data_df = pd.DataFrame(reservations_data['reservations'])
  room_reservas_df = pd.DataFrame(reservations_data['room_reservas'])
  customers_df = pd.DataFrame(reservations_data['customers'])

  room_info_df = pd.DataFrame(room_info)

  # Getting customer_ids and calling api for getting information
  customer_ids = customers_df['id_customer'].tolist()
  customer_data = [get_customer_info(customer_id) for customer_id in customer_ids]

  customer_data_info_df = pd.DataFrame(customer_data)

  # Return dataframes
  return {
      'reservations': reservations_data_df,
      'room_reservas': room_reservas_df,
      'room_info' : room_info_df,
      'customers': customers_df,
      'customer_data_info': customer_data_info_df
  }

# Example usage with more specific filtering
created_start = datetime.date(2024, 8, 15)
created_end = datetime.date(2024, 8, 20)
arrival_start = datetime.date(2024, 8, 15)
arrival_end = datetime.date(2024, 12, 31)


dataframes_list = []
start_date = created_start

while start_date <= created_end:
    # Calcular la fecha de fin del período 
    loop_date = start_date 
   
    # Asegurarse de que biweekly_end_date no exceda la fecha de fin general
    loop_date = min(loop_date, created_end)
    
    
    dataframes = get_data_for_period( start_date,  loop_date,arrival_start,arrival_end)
    
    print(dataframes)    
    dataframes_list.append(dataframes)
    
    # Actualizar start_date para el siguiente período quincenal
    start_date = loop_date + datetime.timedelta(days=1)
    



import pandas as pd
import os

def save_all_dataframes_to_csv(dataframes_list,output_directory):
    """
    Guarda todos los DataFrames en archivos CSV separados con nombres descriptivos.

    Args:
        dataframes_list (list): Lista de diccionarios, cada uno conteniendo los dataframes.
        output_directory (str): Directorio donde se guardarán los archivos CSV.
    """

    counter = 1
    for dataframes in dataframes_list:
        for dataframe_name, dataframe in dataframes.items():
            
            filename = f"{dataframe_name}_{counter}.csv" 
            filepath = os.path.join(output_directory, filename)
            dataframe.to_csv(filepath,index=False)

        counter += 1   





output_directory = "data_agosto_def"  # Cambia esto por la ruta de tu directorio de salida

print("La lista de dataframes:")

save_all_dataframes_to_csv(dataframes_list,output_directory)

