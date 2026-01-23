from pydantic import Field, StringConstraints
from typing import Annotated
from datetime import datetime

IATAcode = Annotated[
    str,
    StringConstraints(pattern=r"^[A-Z]{3}$", strip_whitespace=True, to_upper=True),
    Field(description="3-letter IATA code of the arrival airport (e.g., 'DXB', 'JFK')")
]

# 2. Mandatory non-empty string for names
CustomerName = Annotated[
    str,
    Field(min_length=1, description="The customer's name to use in the greeting. Default to 'Traveller' if unknown.")
]

# 3. Numeric range for search windows
SearchWindow = Annotated[
    int,
    Field(ge=1, le=30, description="Search window in days (1-30)")
]

DateTime = Annotated[
    datetime,
    Field(description="The date in YYYY-MM-DD format")
]

TripId = Annotated[
    str,
    Field(description="The active Trip ID from greet_customer")
]