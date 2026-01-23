import dataclasses
import uuid
from dataclasses import field
from datetime import datetime, timedelta, date
from typing import Annotated

from bson import ObjectId
from mcp.server import FastMCP
from pydantic import Field

from data_generator.airport_transfers import AirportTransfers
from data_generator.flights import Flights
from data_generator.hotels import Hotels
from data_generator.local_attractions import LocalAttractions
from data_generator.itineraries import Itineraries
from entities.attraction import Attraction
from entities.flight import Flight
from entities.hotel import Hotel
from entities.transfer import Transfer
from tools.mcp_tool import mcp_tool
from tools.standard_response import standard_response
from validators.attractions_validator import validate_attractions
from validators.entity_validator import validate_entity
from validators.hotel_validator import validate_hotel_room_type
from validators.property_validators import CustomerName, IATAcode, DateTime, TripId
from validators.xfer_validator import validate_xfer


@dataclasses.dataclass
class TravelServiceDeps:
    hotels: Hotels = field(default_factory=Hotels)
    flights: Flights = field(default_factory=Flights)
    itineraries: Itineraries = field(default_factory=Itineraries)
    attractions: LocalAttractions = field(default_factory=LocalAttractions)
    transfers: AirportTransfers = field(default_factory=AirportTransfers)
    mcp: FastMCP = field(default_factory=FastMCP)

class TravelService:
    def __init__(self, deps: TravelServiceDeps):
        self.deps = deps

    @mcp_tool
    @standard_response
    async def greet_customer(
            self,
            name: CustomerName = 'Traveller'):
        """
        Generate a warm, professional greeting for the customer.
        This should be the first tool called in a new session to establish rapport.
        """
        # Quick counts to show the AI what's available
        f_count = self.deps.flights.collection.count_documents({})
        h_count = self.deps.hotels.collection.count_documents({})

        trip_id = self._get_trip_id()
        self.deps.itineraries.save_itineraries(trip_id, {'name': name})

        greeting = (
            f"Hello {name}! I am your AI Travel Assistant.\n"
            f"I currently have access to {f_count} flights and {h_count} hotels "
            "across 20 global hubs \n. How can I help you plan your trip today? \n"
            f"**IMPORTANT:** Agent, use trip_id='{trip_id}' for all subsequent tool calls."
        )

        return greeting

    @mcp_tool
    @standard_response
    @validate_entity(arg_name="trip_id", dep_name='itineraries')
    async def search_flights(
            self,
            origin: IATAcode,
            destination: IATAcode,
            travel_date: DateTime,
            trip_id: TripId,
            flexibility_days: Annotated[int, Field(description="Number of days after travel_date to include in the search")] = 1,
    ):
        """
        Finds available flights between two cities with detailed pricing and timing.
        """

        self.deps.itineraries.save_itineraries(trip_id,
                                               {
                                                "origin": origin,
                                                "destination": destination,
                                                "travel_date": travel_date
                                               }
                                            )

        if isinstance(travel_date, date) and not isinstance(travel_date, datetime):
            travel_date = datetime.combine(travel_date, datetime.min.time())

        query = {
            "source_city": origin,
            "destination_city": destination,
            "departure": {"$gte": travel_date, "$lte": travel_date + timedelta(days=flexibility_days)}
            }

        cursor = self.deps.flights.collection.find(query).sort("departure", 1).limit(5)
        results = list(cursor)

        if not results:
            return f"No flights found from {origin} to {destination} on or shortly after {travel_date.date()}."

            # 3. Map to Data Classes
        flight_objects = [Flight.from_dict(f) for f in results]

        # 4. Format response for the LLM
        response = [f"✈️ Flights from {origin.upper()} to {destination.upper()}\n"]

        for f in flight_objects:
            # 3. Format the Rich Text block
            line = (
                f"REF: {f._id}\n"
                f"**{f.carrier}**\n"
                f"   🕒 Departs: {f.departure.strftime('%H:%M')} | Arrives: {f.arrival.strftime('%H:%M')}\n"
                f"   ⏳ Duration: {f.duration}n"
                f"   💰 Fare: {f.fare}\n"
                "--------------------------"
            )
            response.append(line)

        #response.append(f'trip id: {trip_id}')

        return "\n".join(response)

    @mcp_tool
    @standard_response
    @validate_entity(arg_name="trip_id", dep_name='itineraries')
    async def search_hotels(self, trip_id: TripId):
        """
        Finds available hotels at the destination city.
        """

        trip = getattr(self, '_injected_itinerarie')
        destination_city = trip.get('destination')

        if not destination_city:
            return f'Please search and select a flight first to search hotels at your destination city.'

        query = {
            'city_hub': destination_city,
        }

        hotels = self.deps.hotels.collection.find(query).sort("star_rating", -1)

        if not hotels:
            return f'No hotels found at {destination_city}.'

        hotel_objects = [Hotel.from_dict(f) for f in hotels]

        # 4. Format response for the LLM
        response = [f"🏨 Hotels found at {destination_city}\n"]

        for f in hotel_objects:
            for r in f.rooms:
                # 3. Format the Rich Text block
                line = (
                    f"REF: {f._id}\n"
                    f"**Name: {f.name}**\n"
                    f'Ratings: { "⭐" * max(0, f.star_rating) } \n'
                    f'Room Type: {r.type} | Base Price: {r.base_price} \n'
                    f'Amenities: {f.amenities}\n'
                    f'Address: {f.address} \n'
                    "--------------------------"
                )
                response.append(line)

        return "\n".join(response)

    @mcp_tool
    @standard_response
    @validate_entity(arg_name="trip_id", dep_name='itineraries')
    @validate_entity(arg_name="flight_id", dep_name='flights',entity_class=Flight)
    async def save_flight_details(self,
                                  trip_id: TripId,
                                  flight_id: Annotated[str, Field(description="the selected flight id from search_flights")]):
        """
        save selected flight details in itinerary.
        """
        flight = getattr(self, '_injected_flight')

        self.deps.itineraries.save_itineraries(trip_id, {'flight_id': ObjectId(flight_id)})

        return f"✅ flight from {flight.source_city} to {flight.destination_city} saved to your itinerary."

    @mcp_tool
    @standard_response
    @validate_entity(arg_name="trip_id", dep_name='itineraries')
    @validate_hotel_room_type
    async def save_hotel_details(self,
                                 trip_id: TripId,
                                 hotel_id: Annotated[str, Field(description='the selected hotel id from the search_hotels')],
                                 room_type: Annotated[str, Field(description='the selected room type from the search_hotels')]):
        """
        save selected hotel details in itinerary.
        """

        hotel = getattr(self, '_injected_hotel')

        self.deps.itineraries.save_itineraries(trip_id, {'hotel_id': ObjectId(hotel_id), 'room_type': room_type})

        return f"✅ {room_type} room at '{hotel.name}' saved to your itinerary."

    @mcp_tool
    @standard_response
    @validate_entity(arg_name="trip_id", dep_name='itineraries')
    async def view_itinerary(self, trip_id: TripId):
        """
        Return the complete itinerary details including flights, hotels, experiences, and transfers.
        """
        trip = getattr(self, '_injected_itinerarie')

        response = [
            f"📅 **Itinerary for {trip.get('name', 'Traveller')}**",
            f"Trip ID: `{trip_id}`",
            "---"
        ]

        # 1. Resolve Flight
        if trip.get('flight_id'):
            flight_doc = self.deps.flights.find_by_id(str(trip.get('flight_id')))
            if flight_doc:
                f = Flight.from_dict(flight_doc)
                response.append(
                    f"✈️ **Flight Details**\n"
                    f"   {f.carrier} | {f.source_city} ➔ {f.destination_city}\n"
                    f"   Departs: {f.departure.strftime('%d %b, %H:%M')} | Arrives: {f.arrival.strftime('%d %b, %H:%M')}\n"
                )

        # 2. Resolve Hotel
        if trip.get('hotel_id'):
            hotel_doc = self.deps.hotels.find_by_id(str(trip.get('hotel_id')))
            if hotel_doc:
                h = Hotel.from_dict(hotel_doc)
                response.append(
                    f"🏨 **Accommodation**\n"
                    f"   **{h.name}** ({trip.get('room_type')} Room)\n"
                    f"   📍 {h.address}\n"
                )

        # 3. Resolve Local Experiences (Attractions)
        attractions = trip.get('attractions', [])
        if attractions:
            # Assuming you have an experiences repository
            attr_docs = list(self.deps.attractions.collection.find({'_id': {'$in': attractions}}))
            exp_list = "\n".join([f"   ✅ {exp.get('name')}" for exp in attr_docs])
            response.append(f"📸 **Local Experiences**\n{exp_list}\n")

        # 4. Resolve Transfers (Ground Transportation)
        transfer_keys = {
            'home_to_airport_xfer': '🚕 Home ➔ Airport',
            'airport_to_hotel_xfer': '🚕 Airport ➔ Hotel'
        }

        transfers_found = False
        transfer_section = ["🚗 **Ground Transfers**"]

        for key, label in transfer_keys.items():
            xfer_id = trip.get(key)
            if xfer_id:
                xfer_doc = self.deps.transfers.find_by_id(str(xfer_id))
                if xfer_doc:
                    transfers_found = True
                    xfer = Transfer.from_dict(xfer_doc)
                    transfer_section.append(f"   {label}: {xfer.provider} ({xfer.vehicle_type})")

        if transfers_found:
            response.append("\n".join(transfer_section) + "\n")

        # Final Check
        if len(response) <= 3:
            return "Your itinerary is currently empty. Let's start by searching for flights!"

        response.append("---")
        response.append("💡 *Need to make changes? You can search for new options to update any part of your trip.*")

        return '\n'.join(response)

    @mcp_tool
    @standard_response
    @validate_entity(arg_name="trip_id", dep_name='itineraries')
    async def search_local_attractions(self, trip_id: TripId):
        """
        Search for top-rated local attractions and experiences.
        """

        trip = getattr(self, '_injected_itinerarie')
        destination = trip.get('destination')

        experiences = [Attraction.from_dict(e) for e in self.deps.attractions.collection.find({"city_hub": destination})]

        if not experiences:
            return f"I couldn't find specific experiences for {destination} yet."

        results = [f"✨ **Top Experiences in {destination}**", "Select the IDs you'd like to add:", "---"]
        for exp in experiences:
            results.append(f"🆔 `{exp._id}` | **{exp.name}**")
            results.append(f"📝 {exp.description} | 💰 {exp.avg_cost_pp}")
            results.append("")

        return "\n".join(results)

    @mcp_tool
    @standard_response
    @validate_entity(arg_name="trip_id", dep_name='itineraries')
    @validate_attractions
    async def save_local_attractions(self,
                                     trip_id: TripId,
                                     attractions: Annotated[list[str], Field(description="List of experience IDs to add to itinerary")]):
        """
        Save selected local attractions to your itinerary.
        Attractions should be passed as a list of IDs.
        """

        if not attractions:
            return "No attractions selected."

        result = self.deps.itineraries.collection.update_one(
            {"_id": trip_id},
            {"$addToSet": {"attractions": {"$each": attractions}}}
        )

        return f"✅ {len(attractions)} attractions successfully saved to your itinerary!"

    async def _handle_transfer_lookup(self, trip_id: TripId, leg_type: str):
        trip = getattr(self, '_injected_itinerarie')
        flight_id = str(trip.get('flight_id'))

        if not flight_id:
            return "❌ Please book your flight first so I can coordinate the transfer timings."

        flight = Flight.from_dict(self.deps.flights.find_by_id(flight_id))

        # 1. Determine Logic based on Leg Type
        is_departure = leg_type in ['home_to_airport', 'hotel_to_airport']

        if is_departure:
            airport_code = trip.get('origin') if 'home' in leg_type else trip.get('destination')
            pickup_dt = flight.departure - timedelta(hours=3)
            route_str = f"{'Home' if 'home' in leg_type else 'Hotel'} ➔ {airport_code}"
            time_label = f"Suggested Pickup: **{pickup_dt.strftime('%H:%M')}** (3h before departure)"
        else:
            airport_code = trip.get('destination') if 'hotel' in leg_type else trip.get('origin')
            pickup_dt = flight.arrival
            route_str = f"{airport_code} ➔ {'Hotel' if 'hotel' in leg_type else 'Home'}"
            time_label = f"Pickup: **{pickup_dt.strftime('%H:%M')}** (Upon arrival)"

        # 2. Query Database
        transfers = [Transfer.from_dict(t) for t in self.deps.transfers.collection.find({'airport_code': airport_code})]

        if not transfers:
            return f"🚕 No pre-arranged transfers found for {airport_code}."

        # 3. Format Response
        title = leg_type.replace('_', ' ').title()
        response = [
            f"🚕 **{title} Options**",
            time_label,
            f"Route: {route_str}",
            "---"
        ]

        for xfer in transfers:
            response.append(f"🆔 `{xfer._id}` | **{xfer.vehicle_type}** ({xfer.category})\n"
                            f"Provider: {xfer.provider} | Features: {', '.join(xfer.features)}\n")

        response.append(f"---\nTrip ID: `{trip_id}`")
        return "\n".join(response)

    @mcp_tool
    @standard_response
    @validate_entity(arg_name="trip_id", dep_name='itineraries')
    async def find_home_airport_transfer(self, trip_id: TripId):
        """
        search cab rides available from home to airport at source city.
        """
        return await self._handle_transfer_lookup(trip_id, 'home_to_airport')

    @mcp_tool
    @standard_response
    @validate_entity(arg_name="trip_id", dep_name='itineraries')
    async def find_airport_hotel_transfer(self, trip_id: TripId):
        """
        search cab rides available from airport to hotel at destination city.
        """
        return await self._handle_transfer_lookup(trip_id, 'airport_to_hotel_xfer')

    @mcp_tool
    @standard_response
    @validate_entity(arg_name="trip_id", dep_name='itineraries')
    @validate_xfer
    async def save_home_airport_transfer(self, trip_id: TripId, transfer_id: str):
        """Save selected home to airport transfer."""
        return await self._save_xfer(trip_id, 'home_to_airport_xfer')

    @mcp_tool
    @standard_response
    @validate_entity(arg_name="trip_id", dep_name='itineraries')
    @validate_xfer
    async def save_airport_hotel_transfer(self, trip_id: TripId, transfer_id: str):
        """Save selected airport to hotel transfer."""
        # Fixed the key from 'airport_to_home' to 'airport_to_hotel'
        return await self._save_xfer(trip_id, 'airport_to_hotel_xfer')

    async def _save_xfer(self, trip_id: TripId, xfer_key: str):
        xfer = getattr(self, '_injected_xfer')
        trip = getattr(self, '_injected_itinerarie')

        if xfer is None:
            return f'no {xfer_key.replace('_', ' ')}s were added'

        self.deps.itineraries.save_itineraries(trip_id, {xfer_key: xfer._id})

        friendly_name = xfer_key.replace('_', ' ').replace('xfer', '').strip().title()
        return f"✅ {friendly_name} ({xfer.vehicle_type}) saved to your itinerary."

    # @validate_entity(arg_name="trip_id", dep_name='itineraries')
    # async def find_hotel_airport_transfer(self, trip_id: TripId):
    #     return await self._handle_transfer_lookup(trip_id, 'hotel_to_airport')
    #
    # @validate_entity(arg_name="trip_id", dep_name='itineraries')
    # async def find_airport_home_transfer(self, trip_id: TripId):
    #     return await self._handle_transfer_lookup(trip_id, 'airport_to_home')

    def _get_trip_id(self):
        return f"TRIP-{uuid.uuid4().hex[:6].upper()}"