import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# Load dataframes (replace 'file_path' with the paths of your CSV files)
reservations = pd.read_csv("data/reservations.csv")
room_reservations = pd.read_csv("data/room_reservations.csv")
room_name = pd.read_csv("data/room_name.csv")

# Perform the first merge (left join) between reservations and room_reservations on 'id' and 'id_reservation_room'
merged_data = reservations.merge(room_reservations, left_on="id", right_on="id_reserva", how="left")
# Drop the duplicate column 'id_reserva' (from room_reservations)
merged_data.drop('id_reserva', axis=1, inplace=True)

# Perform the second merge with room_name on 'id_room' and 'id' (from room_name)
merged_data = merged_data.merge(room_name, left_on="id_zak_room", right_on="id", how="left")
merged_data.drop('id_y', axis=1, inplace=True)

print(merged_data)

# Convert dates to datetime format
merged_data["start_date"] = pd.to_datetime(merged_data["start_date"], dayfirst=True)
merged_data["end_date"] = pd.to_datetime(merged_data["end_date"], dayfirst=True)

# Calculate daily price by dividing total_price by the stay duration in days
merged_data["days_stay"] = (merged_data["end_date"] - merged_data["start_date"]).dt.days
merged_data["daily_price"] = merged_data["total_price"] / merged_data["days_stay"]

# Rename columns for clarity
merged_data = merged_data.rename(columns={
    "id_x": "reservation_id",
    "id_zak_room": "room_id",
    "id_zak_room_type": "previous_assigned_room_type_id",
    "id_name_type": "room_type_name"
})

# Remove rows where room_type_name is 'TBC' (Not commercialized)
merged_data = merged_data[merged_data['room_type_name'] != 'TBC']

print(merged_data["daily_price"])

sns.boxenplot(x='daily_price', y='room_type_name', data=merged_data)
plt.show()

def adjust_outliers(df, column, group, upper_percentile=80, lower_percentile=20):
    """
    Adjusts values below the lower percentile or above the upper percentile within each group.

    Args:
        df: DataFrame with data.
        column: Name of the numeric column to adjust.
        group: Name of the column to group data by.
        upper_percentile: Upper percentile to cap values (default, 80%).
        lower_percentile: Lower percentile to floor values (default, 20%).

    Returns:
        A new DataFrame with adjusted values.
    """

    # Group data and calculate statistics for each group
    grouped = df.groupby(group)
    upper_bounds = grouped[column].quantile(upper_percentile / 100)
    lower_bounds = grouped[column].quantile(lower_percentile / 100)
    medians = grouped[column].median()

    # Function to replace values
    def replace_values(x, upper_bounds, lower_bounds, medians):
        mask = (x < lower_bounds[x.name]) | (x > upper_bounds[x.name])
        x[mask] = medians[x.name]
        return x

    # Apply function to each group
    df[column] = grouped[column].transform(replace_values, 
                                           upper_bounds=upper_bounds, 
                                           lower_bounds=lower_bounds, 
                                           medians=medians)
    return df

merged_data = adjust_outliers(merged_data, 'daily_price', 'room_type_name')

print("Merged Data after the function")
print(merged_data)


# Checking everything is ok
sns.boxenplot(x='daily_price', y='room_type_name', data=merged_data)
plt.show()

# Cleaning customers data

customers_reservations = pd.read_csv("data/customers_reservations.csv")
customers_data = pd.read_csv("data/customers_data.csv")

customers_reservations.drop(['id_zak_room','id_zak_reservation_room','id_zak_room_type'], axis=1, inplace=True)
customers_data = customers_data[['customer_id','country','creation_date','born_date']]


# Creating output directory
output_dir = "output_data"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)


merged_data.to_csv(  os.path.join(output_dir,"reservations_cleaned.csv"), index=False, sep=",", float_format='%.0f')


customers_reservations.to_csv(  os.path.join(output_dir,"customers_reservations.csv"), index=False, sep=",", float_format='%.0f')
customers_data.to_csv( os.path.join(output_dir,"customers_data.csv"), index=False, sep=",", float_format='%.0f')
