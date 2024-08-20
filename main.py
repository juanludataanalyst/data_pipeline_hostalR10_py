from api_calls import  get_reservations_data, get_room_name_type, get_customer_info
from save_data_funcionts import save_dataframes_to_csv

import pandas as pd

# Define filter parameters
created = {'from': '01/08/2023', 'to': '15/08/2024'}
arrival = {'from': '14/08/2024', 'to': '15/08/2024'}

# Calling apis for reservations and room names
reservations_data = get_reservations_data(created,arrival)
room_info = get_room_name_type()

# Converting raw data to dataframes
reservations_data_df = pd.DataFrame(reservations_data['reservations'])
room_reservas_df = pd.DataFrame(reservations_data['room_reservas'])
customers_df = pd.DataFrame(reservations_data['customers'])
room_info_df = pd.DataFrame(room_info)

# Getting customer_ids and calling api for getting information
customer_ids = customers_df['id_customer'].tolist()  # Get customer id's list from customer dataframe
customer_data = [get_customer_info(customer_id) for customer_id in customer_ids] # List comprension, for iteration and get a dictionary list

customer_data_info_df = pd.DataFrame(customer_data)


dataframes = {
    'reservations': reservations_data_df,
    'room_reservas': room_reservas_df,
    'customers': customers_df,
    'customer_data_info': customer_data_info_df
}

save_dataframes_to_csv(dataframes, 'data')