from dataclasses import dataclass
from typing import List, Optional

@dataclass
class HotelRoom:
    type: str
    base_price: int

@dataclass
class Hotel:
    city_hub: str
    name: str
    category: str
    star_rating: int
    amenities: List[str]
    rooms: List[HotelRoom]
    address: str
    contact: str
    _id: Optional[str] = None

    @classmethod
    def from_dict(cls, data):
        # Handle nested list of HotelRoom objects
        data['rooms'] = [HotelRoom(**r) for r in data.get('rooms', [])]
        if '_id' in data:
            data['_id'] = str(data['_id'])
        return cls(**data)