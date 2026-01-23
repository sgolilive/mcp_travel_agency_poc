import random

from pymongo import IndexModel

from data_generator.local_attractions import TravelMongoClient

class Hotels(TravelMongoClient):
    def __init__(self):
        super().__init__('hotel_details')

        self.collection.create_indexes([
            IndexModel([("city_hub", 1), ("star_rating", -1)]),
            IndexModel([("city_hub", 1), ("category", 1)])
        ])

    def generate_hotel_data(self):

        brands = {
            "Luxury": ["Ritz-Carlton", "Four Seasons", "Taj", "St. Regis", "Park Hyatt"],
            "Midscale": ["Marriott", "Hilton", "Novotel", "Crowne Plaza", "Holiday Inn"],
            "Budget": ["ibis", "Hampton Inn", "Comfort Inn", "Premier Inn", "Ginger"]
        }

        amenities_pool = [
            "Free WiFi", "Swimming Pool", "Fitness Center", "Complimentary Breakfast",
            "Airport Shuttle", "Business Center", "Spa", "Pet Friendly", "24/7 Room Service"
        ]

        hotel_data = []

        for hub in self.hubs:
            for category, brand_list in brands.items():
                # Create ~25 hotels per category per hub
                for i in range(25):
                    brand = random.choice(brand_list)
                    name = f"{brand} {hub} {random.choice(['Grand', 'Suites', 'Residency', 'Plaza', 'View'])}"

                    # Dynamic pricing based on category
                    price_range = {
                        "Luxury": (15000, 50000),
                        "Midscale": (5000, 14000),
                        "Budget": (2000, 4500)
                    }
                    min_p, max_p = price_range[category]

                    hotel = {
                        "city_hub": hub,
                        "name": name,
                        "category": category,
                        "star_rating": 5 if category == "Luxury" else (4 if category == "Midscale" else 3),
                        "amenities": random.sample(amenities_pool, random.randint(3, 6)),
                        "rooms": [
                            {"type": "Standard", "base_price": random.randint(min_p, max_p)},
                            {"type": "Deluxe", "base_price": int(random.randint(min_p, max_p) * 1.4)}
                        ],
                        "address": f"{random.randint(1, 999)} Airport Road, {hub} Area",
                        "contact": f"+{random.randint(10, 99)}-{random.randint(1000, 9999)}"
                    }
                    hotel_data.append(hotel)

        self.insert_records(hotel_data)