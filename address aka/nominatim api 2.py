import openpyxl
import requests

def standardize_address(address):
    api_key = 'Your_Bing_Maps_API_Key'
    base_url = 'https://dev.virtualearth.net/REST/v1/Locations'

    query_params = {
        'query': address,
        'includeNeighborhood': 1,
        'maxResults': 1,
        'key': api_key
    }

    response = requests.get(base_url, params=query_params)
    data = response.json()

    if 'resourceSets' in data and len(data['resourceSets']) > 0 and 'resources' in data['resourceSets'][0]:
        resources = data['resourceSets'][0]['resources']
        if resources:
            location = resources[0]
            standardized_address = {
                'house_number': location.get('address', {}).get('addressLine', ''),
                'road': location.get('address', {}).get('addressLine', ''),
                'city': location.get('address', {}).get('locality', ''),
                'state': location.get('address', {}).get('adminDistrict', ''),
                'country': location.get('address', {}).get('countryRegion', ''),
                'postcode': location.get('address', {}).get('postalCode', '')
            }
            return standardized_address.upper()
    return None

def get_aka_names(address):
    url = f"https://nominatim.openstreetmap.org/search?format=json&q={address}"
    response = requests.get(url)
    data = response.json()
    aka_names = set()
    for entry in data:
        if 'display_name' in entry:
            aka_names.add(entry['display_name'])
    return aka_names

def process_excel(input_file, output_file):
    wb = openpyxl.load_workbook(input_file)
    ws = wb.active

    output_wb = openpyxl.Workbook()
    output_ws = output_wb.active
    output_ws.append(["Original Address", "Standardized Address", "Aka Count", "All Aka Names"])

    for row in ws.iter_rows(min_row=2, values_only=True):
        original_address = row[0]
        standardized_address = standardize_address(original_address)
        aka_names = get_aka_names(standardized_address)
        aka_count = len(aka_names)
        output_ws.append([original_address, standardized_address, aka_count, ", ".join(aka_names)])

    output_wb.save(output_file)

if __name__ == "__main__":
    input_file = "manhattan_test.xlsx"
    output_file = "manhattan_test_output.xlsx"
    process_excel(input_file, output_file)
