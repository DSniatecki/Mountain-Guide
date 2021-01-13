from datetime import date
from typing import Optional
from pydantic.main import BaseModel

from .Destination import Destination


class Section(BaseModel):
    id: int
    name: str
    gotPoints: int
    length: float
    startDestination: Destination
    endDestination: Destination
    isOpen: bool = True
    openingDate: Optional[date]
    closureDate: Optional[date]

    def __hash__(self) -> int:
        return self.id
