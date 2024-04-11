import requests
import pandas as pd

# Set up your Google Maps API key
API_KEY = 'YOUR_API_KEY'  # Replace 'YOUR_API_KEY' with your actual API key

# Function to extract address components
def extract_address_components(address):
    # Construct the request URL
    url = f'https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={API_KEY}'
    
    # Send the request
    response = requests.get(url)
    data = response.json()

    # Extract components if request successful
    if data['status'] == 'OK':
        components = data['results'][0]['address_components']
        address_dict = {}
        for component in components:
            types = component['types']
            for type_ in types:
                if type_ not in address_dict:
                    address_dict[type_] = component['long_name']
        return address_dict
    else:
        print("Geocoding failed for address:", address)
        return None

# Read Excel file containing addresses
excel_file_path = 'addresses.xlsx'  # Update with your file path
df = pd.read_excel(excel_file_path)

# Extract components for each address
address_components_list = []
for index, row in df.iterrows():
    address = row['Address']
    components = extract_address_components(address)
    if components:
        address_components_list.append(components)

# Create DataFrame from the extracted components
address_components_df = pd.DataFrame(address_components_list)

# Concatenate with original DataFrame
df_with_components = pd.concat([df, address_components_df], axis=1)

# Save the DataFrame to a new Excel file
output_excel_path = 'addresses_with_components.xlsx'
df_with_components.to_excel(output_excel_path, index=False)
print("Address components extracted and saved to:", output_excel_path)
