import pandas as pd

# Load the raw data
raw_data = pd.read_excel('storti_data.xlsx')

# Create a dictionary to map raw column names to standardized column names
column_mapping = {
    'ID': 'ID',
    'address': 'Address',
    'accessible': 'Accessible',
    'Meter Number': 'Meter_Number',
    'Meter Location': 'Meter_Location'
}

# Create a new DataFrame with standardized column names
standardized_data = pd.DataFrame(columns=column_mapping.values())

# Iterate through each row in the raw data
for index, row in raw_data.iterrows():
    # Extract relevant information from the row
    id_value = row['ID']
    meter_numbers = row['Meter Number']
    meter_locations = row['Meter Location']

    # Split multiple Meter Numbers and Meter Locations into lists
    meter_numbers_list = str(meter_numbers).split(',')
    meter_locations_list = str(meter_locations).split(',')

    # Create a dictionary with standardized column names and values
    data_dict = {
        'ID': id_value,
        'Address': row['address'],
        'Accessible': row['accessible'],
        'Meter_Number': ','.join(meter_numbers_list),
        'Meter_Location': ','.join(meter_locations_list)
    }

    # Add a row to the standardized data DataFrame
    standardized_data = standardized_data.append(data_dict, ignore_index=True)

# Write the standardized data to a new Excel file
standardized_data.to_excel('standardized_storti_data.xlsx', index=False)
