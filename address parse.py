
import pandas as pd
import re

# Load the Excel files
address_df = pd.read_excel('Book2_11dec.xlsm')
street_mapping_df = pd.read_excel('Copy of Dictionary master (1).xlsx', sheet_name='Street Names')
artery_mapping_df = pd.read_excel('Copy of Dictionary master (1).xlsx', sheet_name='Art')

# Initialize an empty list to store processed data
processed_data = []

# Iterate through each row of the address DataFrame
for index, row in address_df.iterrows():
    address = str(row['COMBO'])
    wr = str(row['ID'])

    # Check if the address should be skipped
    if pd.isna(address) or "SKIP" in str(address):
        continue  # Skip this address and move to the next iteration

    # Extract house number, compass, street name, and artery name
    #house_number_match = re.search(r'^[\d-]+', address)
    house_number_match = re.search(r'^[A-Z\d-]+', address)
    house_number = house_number_match.group() if house_number_match is not None else ''

    # Extract compass point if present in the address
    compass_point_match = re.search(r'(?<!\w)([NESW]|North|East|South|West)(?!\w)', address, re.IGNORECASE)
    compass_point = compass_point_match.group() if compass_point_match else ''

    # Split the address into words
    address_words = address.split()

    # Extract the last word as the artery name
    artery_name = address_words[-1] if address_words else ''

    # Remove the last word from the address_words list
    address_words = address_words[:-1]

    # # Extract street name from the remaining words
    # street_name = ' '.join(address_words)

    # Extract street name from the remaining words without house number and compass
    street_name = ' '.join([word for word in address_words if word not in [house_number, compass_point]])

    # Include first letter of street name if it's the same as compass
    if compass_point and street_name.lower().startswith(compass_point.lower()):
        street_name = street_name[len(compass_point):].strip()

    # If compass is present, try to capture the street name after compass and before artery
    if compass_point and not street_name:
        street_name_match = re.search(rf'{compass_point}\s*(\w+)\s+[A-Z]+', address, re.IGNORECASE)
        street_name = street_name_match.group(1) if street_name_match else ''

    # Find replacement for street name using mapping
    street_mapping = street_mapping_df.set_index('StreetName')['Standard Notation'].to_dict()
    if street_name.upper() in street_mapping:
        street_name = street_mapping[street_name.upper()]

    artery_mapping = artery_mapping_df.set_index('StreetNamePostType')['Standard Notation'].to_dict()
    if artery_name.upper() in artery_mapping:
        artery_name = artery_mapping[artery_name.upper()]

    # Append the processed data to the list
    processed_data.append([wr, house_number, compass_point, street_name, artery_name, address])

# Create a new DataFrame with processed data
processed_df = pd.DataFrame(processed_data, columns=['ID','House Number', 'Compass', 'Street Name', 'Artery Name', 'ADDRESS'])

# Write the processed DataFrame to a new Excel file
processed_df.to_excel('BOOK2_11DEC_SEPARATED.xlsx', index=False)
