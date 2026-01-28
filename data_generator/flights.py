from datetime import datetime, timedelta
import random

from db.flights_mongo_client import FlightsMongoClient
from db.hubs_mongo_client import HubsMongoClient


def generate_flight_data(hubs: HubsMongoClient, flights: FlightsMongoClient):
    carriers = [
        "Air India", "IndiGo", "Vistara", "Emirates", "Qatar Airways",
        "Singapore Airlines", "Lufthansa", "British Airways", "Delta", "United"
    ]

    flight_data = []

    all_hubs = hubs.find_all_hubs()
    # Generate flights for the next 14 days to increase volume
    for day in range(1, 15):
        current_day = datetime.now() + timedelta(days=day)

        # Create a mesh: every hub to 5 other random hubs
        for source in all_hubs:
            # Pick 5 random destinations that aren't the source
            destinations = random.sample([h for h in all_hubs if h != source], 5)

            for dest in destinations:
                # 3 flights per route per day (Morning, Afternoon, Evening)
                for slot in ["Morning", "Afternoon", "Evening"]:
                    hour_range = {"Morning": (6, 11), "Afternoon": (12, 17), "Evening": (18, 23)}
                    h_start, h_end = hour_range[slot]

                    dep_time = current_day.replace(
                        hour=random.randint(h_start, h_end),
                        minute=random.choice([0, 15, 30, 45]),
                        second=0, microsecond=0
                    )

                    # Arrival logic (accounting for long-haul flights)
                    duration_hours = random.randint(2, 15)
                    arrival_time = dep_time + timedelta(hours=duration_hours)

                    flight = {
                        "source_city": source,
                        "destination_city": dest,
                        "departure": dep_time,
                        "arrival": arrival_time,
                        "carrier": random.choice(carriers),
                        "fare": f"₹{random.randint(8000, 95000):,}",
                        "flight_info": {
                            "aircraft": random.choice(["Airbus A350", "Boeing 787", "Boeing 777-300ER"]),
                            "class": random.choice(["Economy", "Business", "First"]),
                            "status": "Scheduled"
                        }
                    }
                    flight_data.append(flight)

    flights.insert_records(flight_data)