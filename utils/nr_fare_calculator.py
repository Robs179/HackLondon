import re

from tfl_fare_calculator import Fare
from bs4 import BeautifulSoup
import urllib


class NRFareManager:
    # All class methods. DO NOT INSTANTIATE!
    @classmethod
    def fare_calculator(cls, origin_code, destination_code, time='0900', date='2025-03-03', railcard=True) -> Fare:
        # Build the URL
        url = 'https://traintimes.org.uk/'
        path = f'{origin_code}/{destination_code}/{time}/{date}'
        time = int(time)
        request_url = url + path
        if railcard:
            request_url += '?railcard=YNG'

        try:
            # Make the request
            req = urllib.request.Request(
                request_url,
                data=None,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
                }
            )
            response = urllib.request.urlopen(req)
            html_content = response.read().decode('utf-8')
        except Exception as e:
            print("Error fetching URL:", e)
            return None

        # Parse the HTML
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find all train results
        train_results = soup.select('li[id^="result"]')

        # Convert input time to minutes
        input_h = time // 100
        input_m = time % 100
        input_total = input_h * 60 + input_m

        qualifying_trains = []
        for result in train_results:
            strong_tag = result.find('strong')
            if not strong_tag:
                continue
            time_text = strong_tag.get_text(strip=True)
            # Split on en dash or hyphen
            departure_time_str = time_text.split('–')[0].strip() if '–' in time_text else time_text.split('-')[0].strip()
            try:
                dep_h, dep_m = map(int, departure_time_str.split(':'))
                dep_total = dep_h * 60 + dep_m
            except:
                continue  # Skip invalid times
            if dep_total >= input_total:
                qualifying_trains.append((dep_total, result))

        if not qualifying_trains:
            return None

        # Sort by departure time and pick the earliest
        qualifying_trains.sort(key=lambda x: x[0])
        earliest_dep_total, earliest_train = qualifying_trains[0]

        # Extract fares
        fares_div = earliest_train.find('div', class_='fares slide')
        if not fares_div:
            return None

        fare_items = fares_div.find_all('li')
        min_price = float('inf')
        min_fare_text = ""
        for fare_li in fare_items:
            fare_text = fare_li.get_text(strip=True)
            # Extract all prices, take the last one
            prices = re.findall(r'£(\d+\.\d{2})', fare_text)
            if not prices:
                continue
            price = float(prices[-1])
            if price < min_price:
                min_price = price
                min_fare_text = fare_text

        if min_price == float('inf'):
            return None

        # Determine peak status
        is_peak = 'Anytime' in min_fare_text

        # Create Fare object
        return Fare(
            origin_code=origin_code,
            destination_code=destination_code,
            cost=min_price,
            is_peak=is_peak,
            is_alternative=False,
            is_nr=True,
            description=min_fare_text.strip()
        )


if __name__ == '__main__':
    fare = NRFareManager.fare_calculator('GTW', 'KGX')
    print(fare)
