from pymongo import IndexModel, ASCENDING

from db.mongo_client import TravelMongoClient

class HubsMongoClient(TravelMongoClient):
    def __init__(self):
        super().__init__('hubs')

        self.collection.create_indexes([
            IndexModel([("iata", ASCENDING)], unique=True),
            IndexModel([("country", ASCENDING)]),
            # Compound index for even faster 'by country' lookup of IATA codes
            IndexModel([("country", ASCENDING), ("iata", ASCENDING)])
        ])

    def find_all_hubs(self) -> list[str]:
        """Returns a flat list of all IATA codes sorted alphabetically."""
        cursor = self.collection.find({}, {'_id': 0, 'iata': 1}).sort('iata', ASCENDING)
        return [doc['iata'] for doc in cursor]

    def find_all_hubs_by_country(self, country: str) -> list[str]:
        """Returns IATA codes for a specific country."""
        # Use a case-insensitive match if you want it to be more robust
        query = {'country': {'$regex': f'^{country}$', '$options': 'i'}}
        cursor = self.collection.find(query, {'_id': 0, 'iata': 1}).sort('iata', ASCENDING)
        return [doc['iata'] for doc in cursor]

    def get_supported_countries(self) -> list[str]:
        """Helpful for the list://countries/supported resource."""
        return sorted(self.collection.distinct('country'))

    def find_hubs_by_city(self, city: str) -> list[str]:
        """Returns all IATA codes for a given city (e.g., 'Tokyo' -> ['HND', 'NRT'])."""
        query = {"city": {"$regex": f"^{city}$", "$options": "i"}}
        cursor = self.collection.find(query, {"_id": 0, "iata": 1})
        return [doc["iata"] for doc in cursor]

