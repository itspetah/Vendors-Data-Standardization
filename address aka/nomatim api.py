import requests
import pandas as pd
import time

# Define API endpoint and user agent
nominatim_url = "https://nominatim.openstreetmap.org/search"
user_agent = "your_application_name/version (your_email@example.com)"  # Replace with your details

output_file = "manhattan_addresses.xlsx"

def get_address_details(address):
    params = {
        "q": address,
        "format": "json",
        "user-agent": user_agent
    }
    response = requests.get(nominatim_url, params=params)
    return response.json()

def process_address(address_data):
    if address_data:
        try:
            address_components = address_data[0]["address"]
            street = address_components.get("road", "")
            housenumber = address_components.get("housenumber", "")
            postcode = address_components.get("postcode", "")
            if street and housenumber:
                full_address = f"{housenumber} {street}, Manhattan, NYC, {postcode}"
                aka_names = []
                for name in address_data:
                    if name.get("display_name") != full_address:
                        aka_names.append(name.get("display_name", ""))
                return full_address, len(aka_names), aka_names
        except KeyError as e:
            print(f"KeyError: {e}. Address data might be missing or in unexpected format.")
    return None, None, None

# Read addresses from Excel file using pandas
address_file = "Manhattan Addresses.xlsx"
df = pd.read_excel(address_file, header=None, names=["Address"])

# Create a new DataFrame to store results
results = []

# Process each address
for address in df["Address"]:
    full_address, aka_name_count, aka_names = process_address(get_address_details(address))
    if full_address:
        results.append([full_address, aka_name_count, ", ".join(aka_names)])
    time.sleep(1)  # Add delay to avoid rate limiting

# Create a DataFrame from the results
results_df = pd.DataFrame(results, columns=["Full Address", "AKA Name Count", "AKA Names"])

# Save results to Excel file
results_df.to_excel(output_file, index=False)

print(f"Addresses and AKA names saved to '{output_file}'.")
