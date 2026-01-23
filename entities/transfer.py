from dataclasses import dataclass
from typing import Optional

@dataclass
class Transfer:
    airport_code: str
    provider: str
    vehicle_type: str
    category: str
    capacity: dict  # Contains passengers, luggage_pieces
    pricing: dict   # Contains base_fare, currency, is_fixed
    features: dict  # Contains meet_and_greet, wait_time, etc.
    rating: float
    _id: Optional[str] = None

    @classmethod
    def from_dict(cls, data):
        return cls(**data)