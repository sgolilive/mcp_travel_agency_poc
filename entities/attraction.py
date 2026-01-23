from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Attraction:
    city_hub: str
    name: str
    type: str  # Sightseeing, Food, Activity
    category: str
    description: str
    rating: float
    avg_cost_pp: int
    details: dict  # Contains must_try, duration, best_time
    tags: List[str]
    _id: Optional[str] = None

    @classmethod
    def from_dict(cls, data):
        return cls(**data)