from datetime import datetime
from typing import Any

from data_generator.mongo_client import TravelMongoClient


class Itineraries(TravelMongoClient):
    def __init__(self):
        super().__init__('itineraries')

    def save_itineraries(self, trip_id: str, fields_to_update: dict[Any, Any]):
        fields_to_update.update({"last_updated": datetime.now()})
        self.collection.update_one(
            {'_id': trip_id},
            {'$set': fields_to_update},
            upsert=True
        )

    # def find_trip(self, trip_id: str):
    #     return self.collection.find_one({'_id': trip_id})