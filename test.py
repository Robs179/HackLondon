import requests

url = "https://api.brfares.com/querysimple?orig=VIC&dest=BTN"

try:
    response = requests.get(url)
    print(f"Status Code: {response.status_code}")  # Print HTTP status
    print(response.text)  # Print raw response
except requests.exceptions.RequestException as e:
    print(f"Error accessing BR Fares API: {e}")