from typing import List
from model.Destination import Destination
from model.Section import Section

from pydantic.main import BaseModel


class Zone(BaseModel):
    id: int
    name: str
    sections: List[Section] = []
    destinations: List[Destination] = []

    def __hash__(self) -> int:
        return self.id
