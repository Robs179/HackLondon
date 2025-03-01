import requests
import json


class Fare:
    origin_code: str
    destination_code: str
    cost: float
    is_peak: bool
    is_alternative: bool
    is_nr: bool

    def __init__(self, origin_code, destination_code, cost, is_peak, is_alternative, is_nr):
        self.origin_code = origin_code
        self.destination_code = destination_code
        self.cost = cost
        self.is_peak = is_peak
        self.is_alternative = is_alternative
        self.is_nr = is_nr

    def __repr__(self):
        return (f"Origin code = {self.origin_code}, Destination code = {self.destination_code}"
                f" Cost = {self.cost}, Is Peak? {self.is_peak}, Is Alternative? {self.is_alternative}, "
                f" Is NR? {self.is_nr}")

class TfLFareManager:
    @classmethod
    def fares_between_stations(cls, origin_code: str, destination_code: str, railcard=False,
                               show_alternative_fares=False) -> list:
        # Assemble the API path
        url = 'https://api.tfl.gov.uk/'
        path = f'/stoppoint/{origin_code}/fareto/{destination_code}'

        request_url = url + path
        if railcard:
            request_url += '?passengerType=Railcard'

        resp = requests.get(request_url)
        data = resp.json()

        fares = []
        for section in data:
            # Set is_alternative based on the header
            header = section.get("header", "")
            is_alternative = header.lower() == "alternate fares".lower()

            # Get origin and destination codes from the journey information
            journey = section.get("journey", {})
            origin_code = journey.get("fromStation", {}).get("atcoCode", "")
            destination_code = journey.get("toStation", {}).get("atcoCode", "")

            # Iterate over each row and then over each ticket available
            for row in section.get("rows", []):
                for ticket in row.get("ticketsAvailable", []):
                    # Convert the cost from string to float
                    cost = float(ticket.get("cost", "0"))
                    # Determine if the ticket is peak based on ticketTime type
                    is_peak = ticket.get("ticketTime", {}).get("type", "").lower() == "peak"

                    # Create a Fare object and add it to the list
                    fare = Fare(origin_code, destination_code, cost, is_peak, is_alternative, False)
                    fares.append(fare)

        # Print the list of Fare objects
        for fare in fares:
            print(fare)

        return fares


if __name__ == '__main__':
    fares = TfLFareManager.fares_between_stations('910GGTWK', '940GZZLUWRR', railcard=True)
    print(fares)