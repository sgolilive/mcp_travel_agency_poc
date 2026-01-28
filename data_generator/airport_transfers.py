import random

from db.airport_xfer_mongo_client import XferMongoClient
from db.hubs_mongo_client import HubsMongoClient


def generate_airport_transfers(hubs: HubsMongoClient, xfers: XferMongoClient):

    transfer_data = []

    vehicle_types = {
        "Private Sedan": {"capacity": 3, "luggage": 2, "category": "Private"},
        "Luxury Chauffeur": {"capacity": 3, "luggage": 3, "category": "Premium"},
        "Private SUV": {"capacity": 6, "luggage": 5, "category": "Private"},
        "Shared Shuttle": {"capacity": 10, "luggage": 1, "category": "Shared"},
        "Airport Express Bus": {"capacity": 40, "luggage": 2, "category": "Public"}
    }

    for hub in hubs.find_all_hubs():
        # Create ~40 transfer options per hub
        for i in range(40):
            v_name, v_info = random.choice(list(vehicle_types.items()))

            # Base price logic (Premium > Private > Shared > Public)
            multiplier = {"Premium": 5, "Private": 3, "Shared": 1, "Public": 0.5}
            base_fare = random.randint(500, 1500) * multiplier[v_info["category"]]

            transfer = {
                "airport_code": hub,
                "provider": f"{hub} {v_info['category']} Transfers Ltd.",
                "vehicle_type": v_name,
                "category": v_info["category"],
                "capacity": {
                    "passengers": v_info["capacity"],
                    "luggage_pieces": v_info["luggage"]
                },
                "pricing": {
                    "base_fare": int(base_fare),
                    "currency": "INR" if hub in ["BOM", "DEL", "BLR"] else "USD",
                    "is_fixed": True
                },
                "features": {
                    "meet_and_greet": v_info["category"] in ["Premium", "Private"],
                    "wait_time_included": "60 mins" if v_info["category"] == "Premium" else "15 mins",
                    "free_cancellation": random.choice([True, False])
                },
                "rating": round(random.uniform(4.2, 5.0), 1)
            }
            transfer_data.append(transfer)

    xfers.insert_records(transfer_data)