from api_calls import get_reservations_data, get_room_name_type, get_customer_info
import pandas as pd
import datetime

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
  print("reservations_data_df ")
  print(reservations_data_df )
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
created_start = datetime.datetime(2024, 1, 1)
created_end = datetime.datetime(2024, 8, 20)
arrival_start = datetime.datetime(2024, 7, 19)
arrival_end = datetime.datetime(2024, 8, 20)


dataframes_list = []
start_date = arrival_start

while start_date <= arrival_end:
    # Calcular la fecha de fin del período quincenal
    loop_date = start_date + datetime.timedelta(days=14)
   
    # Asegurarse de que biweekly_end_date no exceda la fecha de fin general
    loop_date = min(loop_date, arrival_end)

      
    dataframes = get_data_for_period( created_start,  created_end,start_date,loop_date)
    print(dataframes)
    dataframes_list.append(dataframes)
    
    # Actualizar start_date para el siguiente período quincenal
    start_date = loop_date + datetime.timedelta(days=1)
    print("start_date")
    print(start_date)



print(dataframes_list)

#dataframes = get_data_for_period(created_start, created_end, arrival_start, arrival_end)