from datetime import date
from typing import Optional
from model.Destination import Destination
from pydantic.main import BaseModel


class Section(BaseModel):
    id: int
    name: str
    gotPoints: float
    length: Optional[float]
    startDestination: Destination
    endDestination: Destination
    isOpen: bool
    openingDate: Optional[date]
    closureDate: Optional[date]

    def __hash__(self) -> int:
        return self.id
