from db.hubs_mongo_client import HubsMongoClient


def generate_hubs_data(hubs_collection: HubsMongoClient):
    hubs = [
        {"iata": "BOM", "city": "Mumbai", "country": "India"},
        {"iata": "DEL", "city": "Delhi", "country": "India"},
        {"iata": "BLR", "city": "Bengaluru", "country": "India"},
        {"iata": "MAA", "city": "Chennai", "country": "India"},
        {"iata": "DXB", "city": "Dubai", "country": "UAE"},
        {"iata": "AUH", "city": "Abu Dhabi", "country": "UAE"},
        {"iata": "JFK", "city": "New York", "country": "USA"},
        {"iata": "SFO", "city": "San Francisco", "country": "USA"},
        {"iata": "ORD", "city": "Chicago", "country": "USA"},
        {"iata": "LAX", "city": "Los Angeles", "country": "USA"},
        {"iata": "MIA", "city": "Miami", "country": "USA"},
        {"iata": "LHR", "city": "London", "country": "UK"},
        {"iata": "SIN", "city": "Singapore", "country": "Singapore"},
        {"iata": "HND", "city": "Tokyo Haneda", "country": "Japan"},
        {"iata": "NRT", "city": "Tokyo Narita", "country": "Japan"},
        {"iata": "SYD", "city": "Sydney", "country": "Australia"},
        {"iata": "MEL", "city": "Melbourne", "country": "Australia"},
        {"iata": "CDG", "city": "Paris", "country": "France"},
        {"iata": "FRA", "city": "Frankfurt", "country": "Germany"},
        {"iata": "MUC", "city": "Munich", "country": "Germany"},
        {"iata": "HKG", "city": "Hong Kong", "country": "Hong Kong"},
        {"iata": "DOH", "city": "Doha", "country": "Qatar"},
        {"iata": "AMS", "city": "Amsterdam", "country": "Netherlands"},
        {"iata": "IST", "city": "Istanbul", "country": "Turkey"},
        {"iata": "YYZ", "city": "Toronto", "country": "Canada"},
        {"iata": "YVR", "city": "Vancouver", "country": "Canada"},
        {"iata": "ICN", "city": "Seoul", "country": "South Korea"},
        {"iata": "PEK", "city": "Beijing", "country": "China"},
        {"iata": "PVG", "city": "Shanghai", "country": "China"},
        {"iata": "CAN", "city": "Guangzhou", "country": "China"},
        {"iata": "GRU", "city": "São Paulo", "country": "Brazil"},
        {"iata": "GIG", "city": "Rio de Janeiro", "country": "Brazil"},
        {"iata": "JNB", "city": "Johannesburg", "country": "South Africa"},
        {"iata": "CPT", "city": "Cape Town", "country": "South Africa"},
        {"iata": "BKK", "city": "Bangkok", "country": "Thailand"},
        {"iata": "SGN", "city": "Ho Chi Minh City", "country": "Vietnam"},
        {"iata": "ZRH", "city": "Zurich", "country": "Switzerland"},
        {"iata": "MAD", "city": "Madrid", "country": "Spain"},
        {"iata": "BCN", "city": "Barcelona", "country": "Spain"},
        {"iata": "FCO", "city": "Rome", "country": "Italy"},
        {"iata": "MXP", "city": "Milan", "country": "Italy"},
        {"iata": "MEX", "city": "Mexico City", "country": "Mexico"},
        {"iata": "CAI", "city": "Cairo", "country": "Egypt"},
        {"iata": "ADD", "city": "Addis Ababa", "country": "Ethiopia"}
    ]

    hubs_collection.insert_records(hubs)
    # for hub in hubs:
    #     hubs_collection.collection.update_one({"iata": hub["iata"]}, {"$set": hub}, upsert=True)