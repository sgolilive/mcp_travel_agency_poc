from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Flight:
    source_city: str
    destination_city: str
    departure: datetime
    arrival: datetime
    carrier: str
    fare: str
    flight_info: dict  # Contains aircraft, class, status
    _id: Optional[str] = None

    @property
    def duration(self) -> str:
        """Computes the travel time and returns a formatted string."""
        diff = self.arrival - self.departure
        total_seconds = int(diff.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        return f"{hours}hours {minutes}minutes"

    @classmethod
    def from_dict(cls, data):
        # Clean up Mongo's _id if present
        if "_id" in data:
            data["_id"] = str(data["_id"])
        return cls(**data)