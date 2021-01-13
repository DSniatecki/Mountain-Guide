from typing import List
from pydantic.main import BaseModel

from .Section import Section


class PlannedTrip(BaseModel):
    id: int
    name: str
    sections: List[Section] = []

    def __hash__(self) -> int:
        return self.id
