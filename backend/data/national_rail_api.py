import requests
import pandas as pd
from bs4 import BeautifulSoup


def fetch_national_rail_fares():
    """
    Fetch fares from National Rail API.
    """
    # ...your API calling logic...
    return {"fare": 3.00}

# Define URL for the fare query
url = "https://www.brfares.com/!expert?orig=ZWS&dest=GTW&period=20250102"

# Set headers to mimic a real browser (prevents blocking)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Fetch the webpage
response = requests.get(url, headers=headers)

# Check if request was successful
if response.status_code == 200:
    # Parse HTML
    soup = BeautifulSoup(response.text, "html.parser")
    print(soup.prettify())

    # Find the fare table
    table = soup.find("table", {"class": "faretable"})

    # Extract headers
    headers = [th.text.strip() for th in table.find_all("th")]

    # Extract row data
    rows = []
    for tr in table.find_all("tr")[1:]:  # Skip header row
        cols = [td.text.strip() for td in tr.find_all("td")]
        rows.append(cols)

    # Convert to pandas DataFrame
    df = pd.DataFrame(rows, columns=headers)

    # Display data
    print(df.head())

else:
    print("Failed to fetch page:", response.status_code)
