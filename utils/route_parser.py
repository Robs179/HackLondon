from tfl_fare_calculator import *


class RouteParser:
    # All class methods. DO NOT INSTANTIATE!

    @classmethod
    def route_finder(cls, origin: str, destination: str) -> [(str, str)]:
        # returns the list of stations, only points of interchange, as a list of tuples
        url = 'https://api.tfl.gov.uk/'
        path = f'Journey/JourneyResults/{origin}/to/{destination}'

        request_url = url + path

        resp = requests.get(request_url)
        data = resp.json()

        station_tuples = []
        # Iterate over journeys in the response
        for journey in data.get("journeys", []):
            journey_tuples = []
            # Iterate over each leg in the journey
            for leg in journey.get("legs", []):
                # Get the departure and arrival stop points
                departure = leg.get("departurePoint", {})
                arrival = leg.get("arrivalPoint", {})

                # Create Station objects from the stop point information.
                # Here we use the "naptanId" as the tfl_code and "commonName" as the station name.
                dep_station = departure.get("naptanId", "")
                arr_station = arrival.get("naptanId", "")

                if not(dep_station == "" or arr_station == ""):
                    # Append the tuple (boarding station, alighting station)
                    journey_tuples.append((dep_station, arr_station))

            if not journey_tuples in station_tuples and not journey_tuples == []:
                station_tuples.append(journey_tuples)

        return station_tuples

if __name__ == "__main__":
    routes = RouteParser.route_finder('910GSTPADOM', '910GWATRLMN')
    print(routes)



