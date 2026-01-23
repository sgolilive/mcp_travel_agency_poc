from datetime import datetime, timedelta
import random

from bson import ObjectId
from pymongo import IndexModel, ASCENDING

from data_generator.mongo_client import TravelMongoClient

class Flights(TravelMongoClient):
    def __init__(self):
        super().__init__('flight_details')

        self.collection.create_indexes([
            IndexModel([("source_city", 1), ("destination_city", 1), ("departure", 1)]),
            IndexModel([("source_city", 1), ("destination_city", 1), ("fare", 1)])
        ])

    def generate_flight_data(self):
        carriers = [
            "Air India", "IndiGo", "Vistara", "Emirates", "Qatar Airways",
            "Singapore Airlines", "Lufthansa", "British Airways", "Delta", "United"
        ]

        flight_data = []
        # Generate flights for the next 14 days to increase volume
        for day in range(1, 15):
            current_day = datetime.now() + timedelta(days=day)

            # Create a mesh: every hub to 5 other random hubs
            for source in self.hubs:
                # Pick 5 random destinations that aren't the source
                destinations = random.sample([h for h in self.hubs if h != source], 5)

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

        self.insert_records(flight_data)

    # def find_flight(self, flight_id):
    #     return self.collection.find_one({"_id": ObjectId(flight_id)})