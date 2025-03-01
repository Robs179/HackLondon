import requests
import json

class Fare:
    origin_code: str
    destination_code: str
    cost: float
    is_peak: bool
    is_alternative: bool
    is_nr: bool

    def __init__(self, origin_code, destination_code, cost, is_peak, is_alternative, is_nr, description):
        self.origin_code = origin_code
        self.destination_code = destination_code
        self.cost = cost
        self.is_peak = is_peak
        self.is_alternative = is_alternative
        self.is_nr = is_nr
        self.description = description

    def __repr__(self):
        return (f"||Origin code = {self.origin_code}, Destination code = {self.destination_code}"
                f" Cost = {self.cost}, Is Peak? {self.is_peak}, Is Alternative? {self.is_alternative}, "
                f" Is NR? {self.is_nr}, Route Description =  {self.description}||")

    def to_json(self):
        return json.dumps(self.__dict__)


class Station:
    tfl_code: str
    name: str
    is_nr: bool
    nr_code: str

    def __init__(self, t, n, nr, nrc = None):
        self.tfl_code = t
        self.name = n
        self.is_nr = nr
        self.nr_code = nrc

    def __repr__(self):
        return f"||TfL code: {self.tfl_code}, NR Code: {self.nr_code}, name = {self.name}, is NR? {self.is_nr}||"

    def to_json(self):
        return json.dumps(self.__dict__)


class TfLFareManager:
    # All methods to be static for organisation purposes. DO NOT INSTANTIATE!
    @classmethod
    def find_fares(cls, origin_code: str, destination_code: str, railcard=False) -> list:
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
                description = row.get("routeDescription", "") if is_alternative else None
                for ticket in row.get("ticketsAvailable", []):
                    # Convert the cost from string to float
                    cost = float(ticket.get("cost", "0"))
                    # Determine if the ticket is peak based on ticketTime type
                    is_peak = ticket.get("ticketTime", {}).get("type", "").lower() == "peak"

                    # Create a Fare object and add it to the list
                    fare = Fare(origin_code, destination_code, cost, is_peak, is_alternative, False, description)
                    fares.append(fare)

        return fares

    @classmethod
    def name_to_code(cls, search_string: str) -> [Station]:
        url = 'https://api.tfl.gov.uk/'
        path = f'Stoppoint/Search/{search_string}?includeHubs=false&modes=tube,dlr,overground,elizabeth-line,national-rail'

        request_url = url + path

        resp = requests.get(request_url)
        data = resp.json()

        stations = []
        # Iterate over each match to create a Station object
        stations = []
        for match in data.get("matches", []):
            # Use the "id" field for tfl_code
            tfl_code = match.get("id", "")
            name = match.get("name", "")

            # Check the modes list to determine if national-rail is included
            modes = match.get("modes", [])
            is_nr = any(mode.lower() == "national-rail" for mode in modes)

            # Set nr_code to None for all stations
            nr_code = None

            # Create the Station object and add it to the list
            station = Station(tfl_code, name, is_nr, nr_code)
            stations.append(station)

        return stations


if __name__ == '__main__':
    fares = TfLFareManager.find_fares('910GWATFDJ', '910GGTWK', railcard=True)
    print(fares)
    stations = TfLFareManager.name_to_code('Stratford')
    print(stations)