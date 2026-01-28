import json

from logger import get_logger
from tools.travel_service import TravelServiceDeps

class TravelResources:
    def __init__(self, deps: TravelServiceDeps):
        self.deps = deps
        self.logger = get_logger(__name__)

    def get_policy(self, topic: str) -> str:
        """Returns specific policy for a given topic."""
        policies = {
            'cancellations': 'No cancellation charge for cancellations prior to 48 hours',
            'payments': 'All payments must be made at the time of booking confirmation.',
            'changes': 'changes allowed upto 24hrs before departure for a $50 fee'
        }
        return policies.get(topic.lower(), 'no policy found for a given topic')

    def get_airports_by_country(self, country: str) -> list[str]:
        """Returns all airport hub codes for a given country."""
        return self.deps.hubs.find_all_hubs_by_country(country)

    def list_supported_countries(self) -> list[str]:
        """Lists all countries that have supported hubs."""
        return self.deps.hubs.get_supported_countries()

    def get_hotels_at_destination_city(self, city: str) -> list[dict]:
        """Returns all hotels located at any of the hub codes associated with a city."""
        # find_hubs_by_city returns a list, e.g., ["HND", "NRT"]
        hub_codes = self.deps.hubs.find_hubs_by_city(city)
        if not hub_codes:
            return []

        query = {"city_hub": {"$in": hub_codes}}
        cursor = self.deps.hotels.collection.find(query, {"_id": 0})
        return list(cursor)

    def get_attractions(self, city: str) -> list[dict]:
        """Returns local attractions for a given city via its hub codes."""
        hub_codes = self.deps.hubs.find_hubs_by_city(city)
        if not hub_codes:
            return []

        query = {"city_hub": {"$in": hub_codes}}
        cursor = self.deps.attractions.collection.find(query, {"_id": 0})
        return list(cursor)

    def get_ground_transfers(self, city: str) -> list[dict]:
        """Returns ground transfer instructions for all airports in a city."""
        hub_codes = self.deps.hubs.find_hubs_by_city(city)
        if not hub_codes:
            return []

        # Assuming the transfer collection uses 'airport_code'
        query = {"airport_code": {"$in": hub_codes}}
        cursor = self.deps.transfers.collection.find(query, {"_id": 0})
        return list(cursor)

    def get_countries(self) -> str:
        cursor = self.deps.hubs.collection.find({}, {'country': 1}).distinct('country')
        return f'supported countries: {', '.join(list(cursor)) }'