from api_calls import get_reservations_data, get_room_name_type, get_customer_info
import pandas as pd
import datetime

def get_data_for_period(created_start, created_end, arrival_start, arrival_end):
  """
  Realiza una llamada a la API en un rango de fechas especificado para los campos created y arrival,
  y devuelve los dataframes.

  Args:
      created_start (datetime.datetime): Fecha de inicio del rango para el campo created.
      created_end (datetime.datetime): Fecha de fin del rango para el campo created.
      arrival_start (datetime.datetime): Fecha de inicio del rango para el campo arrival.
      arrival_end (datetime.datetime): Fecha de fin del rango para el campo arrival.

  Returns:
      dict: Diccionario con los cuatro dataframes: reservations, room_reservas, customers, customer_data_info.
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
created_start = datetime.datetime(2024, 8, 19)
created_end = datetime.datetime(2024, 8, 20)
arrival_start = datetime.datetime(2024, 8, 19)
arrival_end = datetime.datetime(2024, 8, 20)

dataframes = get_data_for_period(created_start, created_end, arrival_start, arrival_end)
print(dataframes)

