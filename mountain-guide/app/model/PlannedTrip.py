from typing import List
from model.Section import Section
from pydantic.main import BaseModel


class PlannedTrip(BaseModel):
    id: int
    name: str
    sections: List[Section] = []

    def __hash__(self) -> int:
        return self.id
