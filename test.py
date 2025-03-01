import requests

url = "https://gw.brfares.com/legacy_ac_loc?term=lds"

try:
    response = requests.get(url, auth = ('ag', '123'))     
    print(f"Status Code: {response.status_code}")  # Print HTTP status
    print(response.text)  # Print raw response
except requests.exceptions.RequestException as e:
    print(f"Error accessing BR Fares API: {e}")