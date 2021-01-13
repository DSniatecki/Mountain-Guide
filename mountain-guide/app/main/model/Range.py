from typing import List
from pydantic.main import BaseModel

from .Zone import Zone


class Range(BaseModel):
    id: int
    name: str
    country: str
    zones: List[Zone] = []

    def __hash__(self) -> int:
        return self.id
