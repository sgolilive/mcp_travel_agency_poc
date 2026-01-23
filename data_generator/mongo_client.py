import os
import pymongo
from bson import ObjectId

from logger import get_logger

class TravelMongoClient:
    def __init__(self, collection_name):
        self.client = pymongo.MongoClient(os.getenv("MONGO_URI"))
        self.db = self.client[os.getenv("MONGO_DB_NAME")]
        self.collection = self.db[collection_name]
        self.collection_name = collection_name

        self.hubs = ["BOM", "DEL", "BLR", "DXB", "SIN", "LHR", "JFK", "SFO", "HND", "SYD",
            "CDG", "FRA", "HKG", "DOH", "AMS", "IST", "YYZ", "ORD", "AUH", "ICN"]

        self.logger = get_logger(collection_name)

    def insert_records(self, data):
        if data:
            self.logger.warn(f"Inserting data into {self.collection_name}")
            self.collection.delete_many({})
            result = self.collection.insert_many(data)
            self.logger.info(f"🌍 Successfully inserted {len(result.inserted_ids)} {self.collection_name.replace('_', ' ')}")
        else:
            self.logger.warn(f"No data inserted into {self.collection_name}")

    def find_by_id(self, the_id: str):
        return self.collection.find_one({"_id": the_id if the_id.startswith("TRIP") else ObjectId(the_id)})

    #query = {
    #"airport_code": "JFK",
    #"capacity.passengers": {"$gte": 4},
    #"capacity.luggage_pieces": {"$gte": 5}
    # }
    # available_rides = list(db.airport_transfers.find(query).sort("pricing.base_fare", 1))

    def search_data(self, query):
        pass

    # def insert_record(self, data):
    #     self.collection.upsert(data)
    #     pass

    def delete_record(self, data):
        self.collection.delete_one({'_id': data.get("id")})