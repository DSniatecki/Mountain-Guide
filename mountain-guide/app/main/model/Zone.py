from typing import List

from pydantic.main import BaseModel

from .Destination import Destination
from .Section import Section


class Zone(BaseModel):
    id: int
    name: str
    sections: List[Section] = []
    destinations: List[Destination] = []

    def __hash__(self) -> int:
        return self.id
