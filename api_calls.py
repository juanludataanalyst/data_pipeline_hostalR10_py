import requests
import json

# Define API details
headers = {'x-api-key': 'wb_3f048daa-4842-11ee-8d46-001a4ae7b219'}




def get_reservations_data(created, arrival):
  
  def fetch_data(created, arrival, pager): # Funcion anidada para que se actualice el pager
    data = {'filters': json.dumps({'created': created, 'arrival': arrival, 'pager': pager})}
    response = requests.post('https://kapi.wubook.net/kp/reservations/fetch_reservations', headers=headers, data=data)
    return json.loads(response.text)  

  reservations_data = []
  room_reserva = []
  customers = []

  pager = {'limit': 20, 'offset': 0}
  has_more_data = True
  while has_more_data: 
    fetched_data = fetch_data(created, arrival, pager)
    reservations = fetched_data['data']['reservations']
    

    if not reservations:
      has_more_data = False
      continue

    for reservation in reservations:
     reserva_data = {
      'id': reservation['id'],
      'status': reservation['status'],
      'total_price': reservation['price']['total'],
      'channel': reservation['origin']['channel'],
      'created_date': reservation['created'] }
     reservations_data.append(reserva_data)


     for room in reservation['rooms']:
      rooms_data = {
          'id_zak_room': room['id_zak_room'],
          'id_zak_reservation_room': room['id_zak_reservation_room'],
          'id_zak_room_type': room['id_zak_room_type'],
          'id_reserva': reservation['id'],
          'start_date': room['dfrom'],
          'end_date': room['dto']
      }
      room_reserva.append(rooms_data)

      for customer in room['customers']:
        customers_data = {
          'id_customer': customer['id'],
          'id_reserva': reservation['id'],
          'id_zak_room': room['id_zak_room'],
          'id_zak_reservation_room': room['id_zak_reservation_room'],
          'id_zak_room_type': room['id_zak_room_type']
        }
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


  return room_info

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

  #respuesta_json['data']['main_info']['customer_id'] = customer_id


