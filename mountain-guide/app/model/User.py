from typing import List
from model.PlannedTrip import PlannedTrip
from pydantic.main import BaseModel


class User(BaseModel):
    id: int
    login: str
    email: str
    password: str
    role: str
    plannedTrips: List[PlannedTrip] = []

    def __hash__(self) -> int:
        return self.id
