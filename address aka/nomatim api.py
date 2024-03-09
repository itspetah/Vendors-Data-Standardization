import requests
import openpyxl
import time

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
                    if name["display_name"] != full_address:
                        aka_names.append(name["display_name"])
                return full_address, len(aka_names), aka_names
        except KeyError as e:
            print(f"KeyError: {e}. Address data might be missing or in unexpected format.")
    return None, None, None

workbook = openpyxl.load_workbook("Manhattan Addresses.xlsx")
sheet = workbook.active

# Assuming addresses are in the first column (column A)
for cell in sheet["A"]:
    address = cell.value
    if address:
        full_address, aka_name_count, aka_names = process_address(get_address_details(address))
        if full_address:
            row = cell.row
            sheet.cell(row=row, column=2).value = full_address
            sheet.cell(row=row, column=3).value = aka_name_count
            sheet.cell(row=row, column=4).value = ", ".join(aka_names)
        time.sleep(1)  # Add delay to avoid rate limiting

workbook.save(output_file)
print(f"Addresses and AKA names saved to '{output_file}'.")
