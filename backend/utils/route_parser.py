from utils.nr_fare_calculator import NRFareManager
import re
import requests
from utils.tfl_fare_calculator import *


class RouteParser:
    # All class methods. DO NOT INSTANTIATE!

    @classmethod
    def route_finder(cls, origin: str, destination: str, time: str) -> [[(str, str)]]:
        # returns the list of stations, only points of interchange, as a list of tuples
        url = 'https://api.tfl.gov.uk/'
        path = f'Journey/JourneyResults/{origin}/to/{destination}?time={time}&modes=tube,dlr,overground,elizabeth-line,national-rail'

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

                # Here we use the "naptanId" as the tfl_code and "commonName" as the station name.
                dep_station = departure.get("naptanId", "")
                arr_station = arrival.get("naptanId", "")

                if not (dep_station == "" or arr_station == ""):
                    # Append the tuple (boarding station, alighting station)
                    journey_tuples.append((dep_station, arr_station))

            if (not journey_tuples in station_tuples) and (not journey_tuples == []):
                station_tuples.append(journey_tuples)

        return cls.combine_lu_legs(station_tuples)

    # where appropriate, combine the journeys of the same type
    # taking advantage that all NR fares start with 910, and non-NR fares start with 940
    @classmethod
    def combine_lu_legs(cls, journeys):
        combined_journeys = []
        for journey in journeys:
            # Discard the journey if any station code does not start with 910 or 940
            if any(not (station.startswith('910') or station.startswith('940'))
                   for leg in journey for station in leg):
                continue

            new_journey = []
            current_non_nr_start = None
            current_non_nr_end = None

            for leg in journey:
                origin, destination = leg
                # Check if the leg is a non-national rail leg (both codes start with 940)
                if origin.startswith('940') and destination.startswith('940'):
                    if current_non_nr_start is None:
                        current_non_nr_start = origin
                    current_non_nr_end = destination
                else:
                    # Flush any accumulated non-national rail segment before processing this leg
                    if current_non_nr_start is not None:
                        new_journey.append((current_non_nr_start, current_non_nr_end))
                        current_non_nr_start = None
                        current_non_nr_end = None
                    new_journey.append(leg)

            # Flush any remaining non-national rail segment at the end of the journey
            if current_non_nr_start is not None:
                new_journey.append((current_non_nr_start, current_non_nr_end))

            combined_journeys.append(new_journey)
        return combined_journeys

    @classmethod
    def journeyTfLFares(cls, journey, time, weekday, railcard) -> [{(str, str): Fare}]:
        """
        Calculates TfL fares for any valid partition by calling TfLFareManager.find_fares.
        Outputs a dictionary with keys as tuples (origin, destination) and values as the lowest non-alternative fare.
        """
        # Determine if the time is during peak hours
        time = int(time)
        peak = (630 <= time <= 930 or 1600 <= time <= 1900) and weekday

        fares_dict = {}
        fares_dict[(journey[0][0], journey[-1][1])] = TfLFareManager.find_fares(journey[0][0], journey[-1][1], railcard)

        # Generate all possible origin-destination pairs
        for i in range(len(journey)):
            origin = journey[i][0]
            for j in range(i, len(journey)):
                destination = journey[j][1]
                # Retrieve all fares for this origin-destination pair
                fares = TfLFareManager.find_fares(origin, destination, railcard)
                # Filter out alternative fares and those not matching peak status
                valid_fares = [
                    fare for fare in fares
                    if not fare.is_alternative and fare.is_peak == peak
                ]
                # Find the minimum cost fare
                if valid_fares:
                    min_fare = min(valid_fares, key=lambda f: f.cost)
                    fares_dict[(origin, destination)] = min_fare
                else:
                    fares_dict[(origin, destination)] = Fare(origin, destination, float('inf'), peak, False, None, None)

        return fares_dict

    @classmethod
    def getTfLDict(cls, origin, destination, time, weekday, railcard):
        routes = RouteParser.route_finder(origin, destination, time)
        prices = []
        for route in routes:
            prices.append(RouteParser.journeyTfLFares(route, time, weekday, railcard))
        return prices

    @classmethod
    def tfl_code_to_name(cls, tfl_code) -> str:
        url = 'https://api.tfl.gov.uk/'
        path = f'stoppoint/{tfl_code}'
        request_url = url + path

        resp = requests.get(request_url)
        data = resp.json()
        common_name = data['commonName']
        # Remove the station type suffix (e.g., Underground Station, DLR Station, Rail Station)
        name = re.sub(r'\s+(Underground|DLR|Rail)\s+Station$', '', common_name)
        name = re.sub(r' ', '%20', name)
        if name == "London%20Gatwick%20Airport":
            name = "Gatwick%20Airport"
        elif name == "Victoria":
            name = "London%20Victoria"

        return name

    @classmethod
    def journeyNRFares(cls, journey, time, weekday, railcard) -> {(str, str): Fare}:
        """
        Calculates National Rail fares for valid partitions of the journey, excluding pairs entirely within non-NR stations.
        """
        fares_dict = {}

        # Generate all possible origin-destination pairs
        for i in range(len(journey)):
            origin_tfl = journey[i][0]
            for j in range(i, len(journey)):
                dest_tfl = journey[j][1]

                # Exclude pairs where both stations are non-National Rail (start with 940)
                if origin_tfl.startswith('940') and dest_tfl.startswith('940'):
                    continue

                # Convert TfL codes to NR names
                origin_nr = cls.tfl_code_to_name(origin_tfl)
                dest_nr = cls.tfl_code_to_name(dest_tfl)

                # Calculate NR fare
                fare = NRFareManager.fare_calculator(
                    origin_nr,
                    dest_nr,
                    time="1600",
                    date='2025-03-04',
                    railcard=True
                )

                # Assuming fare is a Fare object with a 'cost' attribute; adjust based on actual implementation
                fares_dict[(origin_tfl, dest_tfl)] = fare

        return fares_dict


    @classmethod
    def getNRDict(cls, origin, destination, time, weekday, railcard):
        routes = RouteParser.route_finder(origin, destination, time)
        prices = []
        for route in routes:
            prices.append(RouteParser.journeyNRFares(route, time, weekday, railcard))
        return prices

    @classmethod
    def find_optimum_fare(cls, origin: str, destination: str, time: str, railcard: bool) -> str:
        def generate_all_splits(route):
            n = len(route)
            splits = []
            for mask in range(0, 1 << (n - 1)):
                current_split = []
                start = 0
                for i in range(n - 1):
                    if mask & (1 << i):
                        end = i + 1
                        current_split.append((start, end))
                        start = end
                current_split.append((start, n))
                segments = []
                for s, e in current_split:
                    origin_segment = route[s][0]
                    dest_segment = route[e - 1][1]
                    segments.append((origin_segment, dest_segment))
                splits.append(segments)
            return splits

        routes = cls.route_finder(origin, destination, time)
        min_total_cost = float('inf')
        optimal_fares = []

        for route in routes:
            tfl_partitions = cls.journeyTfLFares(route, time, True, True)
            nr_partitions = cls.journeyNRFares(route, time, True, True)

            # Collect minimum TfL fares for each segment
            tfl_fares = {}
            for segment in tfl_partitions.keys():
                fare = tfl_partitions[segment]
                if segment not in tfl_fares or fare.cost < tfl_fares[segment].cost:
                    tfl_fares[segment] = fare

            # Collect minimum NR fares for each segment
            nr_fares = {}
            for segment in nr_partitions:
                fare = nr_partitions[segment]
                if segment not in nr_fares or fare.cost < nr_fares[segment].cost:
                    nr_fares[segment] = fare

            # Combine to get the minimum fare (TfL or NR) for each segment
            combined_fares = {}
            all_segments = set(tfl_fares.keys()).union(nr_fares.keys())
            for segment in all_segments:
                tfl_fare = tfl_fares.get(segment)
                nr_fare = nr_fares.get(segment)
                if tfl_fare and nr_fare:
                    combined_fares[segment] = tfl_fare if tfl_fare.cost < nr_fare.cost else nr_fare
                elif tfl_fare:
                    combined_fares[segment] = tfl_fare
                elif nr_fare:
                    combined_fares[segment] = nr_fare

            splits = generate_all_splits(route)
            for split in splits:
                total_cost = 0
                current_fares = []
                valid = True
                for seg in split:
                    fare = combined_fares.get(seg)
                    if not fare:
                        valid = False
                        break
                    total_cost += fare.cost
                    current_fares.append(fare)
                if valid and total_cost < min_total_cost:
                    min_total_cost = total_cost
                    optimal_fares = current_fares

        return cls.compile_fares_to_json(optimal_fares)

    @classmethod
    def compile_fares_to_json(cls, fares_list):
        """
        Compiles a list of Fare objects into a single JSON array.
        Each Fare object is converted using its to_json() method.
        """
        # Convert each Fare object to its JSON representation and parse into a dict
        fares_data = [json.loads(fare.to_json()) for fare in fares_list]

        # Convert the list of dicts to a formatted JSON string
        return json.dumps(fares_data, indent=2)


if __name__ == "__main__":
    print(RouteParser.find_optimum_fare('940GZZLUGDG', '910GGTWK', "1630", False))