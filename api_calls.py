import requests
import json
import pandas as pd
from dotenv import load_dotenv
import os
import datetime

# Loads environment variables from the .env file
load_dotenv('.env')

# Accesses API KEY environment variable
api_key = os.getenv('API_KEY')

# Define API KEY in dictionary
headers = {'x-api-key': api_key}

def get_reservations_data(created, arrival):
  
  def fetch_data(created, arrival, pager): # Funcion anidada para que se actualice el pager
    data = {'filters': json.dumps({'created': created, 'arrival': arrival, 'pager': pager})}
    response = requests.post('https://kapi.wubook.net/kp/reservations/fetch_reservations', headers=headers, data=data)
    return json.loads(response.text)  

  reservations_data = []
  room_reserva = []
  customers = []
  
  unique_reservation_ids_for_reservations = [] # Save reservations id to avoid duplicates from API
  unique_reservation_ids_for_rooms = []
  unique_reservation_ids_for_customers = []


  pager = {'limit': 1, 'offset': 0}
  has_more_data = True
  while has_more_data:
    print("El pager es:", pager)
    fetched_data = fetch_data(created, arrival, pager)
    reservations = fetched_data['data']['reservations']
    print(created, arrival, pager)
    #print(reservations)

    if not reservations:
      has_more_data = False
      continue

    import pandas as pd

    for  i in range(len(reservations)):
     reservation = reservations[i]
     reserva_data = {
      'id': reservation['id'],
      'status': reservation['status'],
      'total_price': reservation['price']['total'],
      'channel': reservation['origin']['channel'],
      'created_date': reservation['created'] }
     if reservation['id'] not in unique_reservation_ids_for_reservations : # Api send duplicates registers, only increase list if it is new
      unique_reservation_ids_for_reservations .append(reservation['id'] )
      reservations_data.append(reserva_data)
     else:
      print("Excluding", reservation['id']," Reserva")  
     print("Unicos element ids ", unique_reservation_ids_for_reservations )  
     print("Elementos en la lista reservations", len(reservations))
     print("Elementos en la lista append:", len(reservations_data))
     print(pd.DataFrame(reservations_data))
     #import time
     #time.sleep(10)

     for room in reservation['rooms']:
      rooms_data = {
          'id_zak_room': room['id_zak_room'],
          'id_zak_reservation_room': room['id_zak_reservation_room'],
          'id_zak_room_type': room['id_zak_room_type'],
          'id_reserva': reservation['id'],
          'start_date': room['dfrom'],
          'end_date': room['dto']
      }
      if reservation['id'] not in unique_reservation_ids_for_rooms : # Api send duplicates registers, only increase list if it is new
        unique_reservation_ids_for_rooms .append(reservation['id'] )
        room_reserva.append(rooms_data)

      for customer in room['customers']:
        customers_data = {
          'id_customer': customer['id'],
          'id_reserva': reservation['id'],
          'id_zak_room': room['id_zak_room'],
          'id_zak_reservation_room': room['id_zak_reservation_room'],
          'id_zak_room_type': room['id_zak_room_type']
        }
        if reservation['id'] not in unique_reservation_ids_for_customers : # Api send duplicates registers, only increase list if it is new
          unique_reservation_ids_for_customers.append(reservation['id'] )
          customers.append(customers_data)
  
 # Update offset for next iteration
    pager['offset'] += pager['limit']
    


  # Return all three DataFrames in a dictionary
  return {
      'reservations': reservations_data,
      'room_reservas': room_reserva,
      'customers': customers
  }

def get_room_name_type():
  response= requests.post('https://kapi.wubook.net/kp/property/fetch_rooms', headers = headers)

  data_rooms = json.loads(response.text)

  room_info = []

  for room in data_rooms['data']:  
    room_data = {
        'id': room['id'],
        'id_room_type': room['id_room_type'],
        'name': room['name']
    } 
    
    room_info.append(room_data)

    
  # Dictionary to map room type
  mapping = {
      15507: 'shared',
      15504: 'shared',
      15505: 'shared',
      23197: 'individual shared bathroom',
      15508: 'double shared bathroom',
      15509: 'double privated bathroom',
    # 15510: 'double privated bathroom e',
      15510: 'double privated bathroom',
      23174: 'double shared bathroom',
      23175: 'individual privated bathroom',
      33902: 'TBC',
      #68222: 'individual private bathroom e'
    68222: 'individual privated bathroom'
      
  }

  room_name = pd.DataFrame(room_info)
   
  room_name['id_name_type'] = room_name['id_room_type'].map(mapping)

  # Cleaning error
  room_name['name'] = room_name['name'].replace('DEBP', '216')


  return room_name

def get_customer_info(customer_id):
  data = {'id': customer_id}
  response = requests.post('https://kapi.wubook.net/kp/customers/fetch_one', headers=headers, data=data)
  response_json = response.json()

  customer_info =  { 
      'customer_id': customer_id,
      'country' : response_json['data']['main_info']['country'],
      'creation_date' : response_json['data']['main_info']['creation'],
      'city' : response_json['data']['main_info']['city'],
      'birth_country' : response_json['data']['anagraphical']['birth_country'],
      'birth_city' : response_json['data']['anagraphical']['gender'],
      'born_date' : response_json['data']['anagraphical']['birthday']
   }                     

  return customer_info

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
  
  # Converting raw data to dataframes
  reservations_data_df = pd.DataFrame(reservations_data['reservations'])
  room_reservas_df = pd.DataFrame(reservations_data['room_reservas'])
  customers_df = pd.DataFrame(reservations_data['customers'])

    # Return dataframes
  return {
      'reservations': reservations_data_df,
      'room_reservas': room_reservas_df,
      'customers': customers_df
  }

def get_reservations_df_list(created_start, created_end, arrival_start, arrival_end):
    dataframes_reservation_list = []  # List for reservations (Dictionaries)
    start_date = created_start

    while start_date <= created_end:
        # Calcular la fecha de fin del período 
        loop_date = start_date 
       
        # Asegurarse de que biweekly_end_date no exceda la fecha de fin general
        loop_date = min(loop_date, created_end)
        
        
        dataframes = get_data_for_period(start_date, loop_date, arrival_start, arrival_end)
        
        if dataframes:  #Add to list if api return something
            dataframes_reservation_list.append(dataframes)
        
        # Actualizar start_date para el siguiente período quincenal
        start_date = loop_date + datetime.timedelta(days=1)
    
    return dataframes_reservation_list

def get_customer_data_df(dataframes_reservation_list):
    all_customer_ids = []
    for df in dataframes_reservation_list:
        if not df['customers'].empty:
            customer_ids = df['customers']['id_customer'].tolist()
            all_customer_ids.extend(customer_ids)
    
    all_customer_ids = list(set(all_customer_ids))
    
    customer_data = [get_customer_info(customer_id) for customer_id in all_customer_ids]
    
    return pd.DataFrame(customer_data)

def get_and_save_all_dataframes():

  created_start = datetime.date(2024, 1, 1)
  #created_start = datetime.date(2022, 12, 30)
  created_end = datetime.date(2024, 8,27)
  arrival_start = datetime.date(2024, 1, 1)
  arrival_end = datetime.date(2024, 12, 31)

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
  
  

  
  os.makedirs("data_2024", exist_ok=True) 
  output_directory = "data_2024"
  
  reservations_df.to_csv(os.path.join(output_directory,"reservations.csv"),index=False, sep=',')
  room_reservation_df.to_csv(os.path.join(output_directory,"room_reservations.csv"),index=False, sep=',')
  customers_reservation_df.to_csv(os.path.join(output_directory,"customers_reservations.csv"),index=False, sep=',')
  room_name_df.to_csv(os.path.join(output_directory,"room_name.csv"),index=False, sep=',')
  customer_data_df.to_csv(os.path.join(output_directory,"customers_data.csv"),index=False, sep=',')

  print("Dataframe Finished")



