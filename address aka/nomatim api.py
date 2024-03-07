import pandas as pd
from geopy.geocoders import Nominatim

# Set up Nominatim Geocoder
geolocator = Nominatim(user_agent="aka_finder")

def find_aka_names(address):
    # Query Nominatim API to find the location details
    location = geolocator.geocode(address)
    if location:
        return location.raw.get('alternate_names', [])

def main(input_file, output_file):
    # Read the Excel file with addresses in Manhattan
    df = pd.read_excel(input_file)
    
    # Initialize lists to store aka names and counts
    aka_names_list = []
    aka_counts = []
    
    # Iterate over each address
    for index, row in df.iterrows():
        address = row['Address']
        aka_names = find_aka_names(address)
        if aka_names:
            aka_names = [name for name in aka_names.split(',')]
        else:
            aka_names = []
        aka_names_list.append(aka_names)
        aka_counts.append(len(aka_names))
    
    # Add aka names and counts to the DataFrame
    df['Aka Names'] = aka_names_list
    df['Aka Count'] = aka_counts
    
    # Write the DataFrame to a new Excel file
    df.to_excel(output_file, index=False)

if __name__ == "__main__":
    input_file = 'manhattan_addresses.xlsx'
    output_file = 'manhattan_aka_addresses.xlsx'
    main(input_file, output_file)
