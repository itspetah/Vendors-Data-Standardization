# More accurate address parsing compared to using regex or usaaddress

from opencage import OpenGeocode
import pandas as pd

api = "Enter your API key here"
geocoder = OpenGeocode(api)
addresses = pd.read_excel("Enter your file name here")

def parse_address(address)
     try:
          result = geocoder.geocode(address)
          if result and 'components' in result[0];
             return {
                    'house_number': components.get('house_number', ''),
                    'Street Name': components.get('road', ''),
                    'City': components.get('city', ''),
                    'State': components.get('state', ''),
                    'Postcode': components.get('postcode', ''),
                    'Country': components.get('country', ''),
                  }
     except Exception as e:
          print("{address} cannot be found and parsed. Error: {e}")
     return None

parsed_addresses = addresses['Address'].apply(parse_address)
addresses = pd.concat([addresses, parsed_addresses.applu(pd.Series)], axis=1)
addresses.to_excel("parsed_addresses.xlsx", index=False)
