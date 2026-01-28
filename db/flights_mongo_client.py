from pymongo import IndexModel
from db.mongo_client import TravelMongoClient

class FlightsMongoClient(TravelMongoClient):
    def __init__(self):
        super().__init__('flights')

        self.collection.create_indexes([
            IndexModel([("source_city", 1), ("destination_city", 1), ("departure", 1)]),
            IndexModel([("source_city", 1), ("destination_city", 1), ("fare", 1)])
        ])