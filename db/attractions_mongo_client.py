from pymongo import IndexModel, TEXT
from db.mongo_client import TravelMongoClient

class AttractionsMongoClient(TravelMongoClient):
    def __init__(self):
        super().__init__('attractions')

        self.collection.create_indexes([
            IndexModel([("city_hub", 1), ("type", 1), ("rating", -1)]),
            IndexModel([("name", TEXT), ("description", TEXT)], name="text_search")
        ])