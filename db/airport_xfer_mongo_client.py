from pymongo import IndexModel
from db.mongo_client import TravelMongoClient

class XferMongoClient(TravelMongoClient):
    def __init__(self):
        super().__init__('xfers')

        self.collection.create_indexes([
            IndexModel([("airport_code", 1), ("capacity.passengers", 1)])
        ])