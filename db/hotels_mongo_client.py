from pymongo import IndexModel

from db.mongo_client import TravelMongoClient


class HotelsMongoClient(TravelMongoClient):
    def __init__(self):
        super().__init__('hotels')

        self.collection.create_indexes([
            IndexModel([("city_hub", 1), ("star_rating", -1)]),
            IndexModel([("city_hub", 1), ("category", 1)])
        ])