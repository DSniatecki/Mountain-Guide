from typing import List
from pydantic.main import BaseModel

from .PlannedTrip import PlannedTrip


class User(BaseModel):
    id: int
    login: str
    email: str
    password: str
    role: str
    plannedTrips: List[PlannedTrip] = []

    def __hash__(self) -> int:
        return self.id
