from typing import List
from model.Zone import Zone
from pydantic.main import BaseModel


class Range(BaseModel):
    id: int
    name: str
    country: str
    zones: List[Zone] = []

    def __hash__(self) -> int:
        return self.id
