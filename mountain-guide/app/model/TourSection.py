from datetime import date
from typing import Optional
from model.Destination import Destination
from pydantic.main import BaseModel


class TourSection(BaseModel):
    id: int
    name: str
    country: str
    rangeName: str
    zoneName: str
    startDestination: Destination
    endDestination: Destination
    gotPoints: int
    length: float
    isOpen: bool

    def __hash__(self) -> int:
        return self.id
