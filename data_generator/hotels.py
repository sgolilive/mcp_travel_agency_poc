import random

from db.hotels_mongo_client import HotelsMongoClient
from db.hubs_mongo_client import HubsMongoClient

def generate_hotel_data(hubs: HubsMongoClient, hotels: HotelsMongoClient):

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

    for hub in hubs.find_all_hubs():
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

    hotels.insert_records(hotel_data)