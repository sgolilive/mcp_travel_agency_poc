from functools import wraps
from entities.hotel import Hotel

def validate_hotel_room_type(func):
    @wraps(func)
    async def wrapper(self, *args, **kwargs):

        hotel_id = kwargs.get("hotel_id")

        hotel = self.deps.hotels.find_by_id(hotel_id)

        hotel_object = Hotel.from_dict(hotel)

        if not hotel:
            return f"❌ No hotel found with id {hotel_id}."

        # 2. Extract allowed types: ["Standard", "Deluxe"]
        allowed_types = [room.type for room in hotel_object.rooms]

        room_type = kwargs.get("room_type")

        # 3. Validation Logic
        if room_type not in allowed_types:
            return (
                f"❌ Invalid room type '{room_type}'. "
                f"Allowed options for this hotel are: {', '.join(allowed_types)}."
            )

        target_key = f"_injected_hotel"
        setattr(self, target_key, hotel_object)
        return await func(self, *args, **kwargs)

    return wrapper