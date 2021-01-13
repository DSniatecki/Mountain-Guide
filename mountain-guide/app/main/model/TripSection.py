from pydantic.main import BaseModel

from .Destination import Destination


class TripSection(BaseModel):
    id: int
    name: str
    country: str
    rangeName: str
    zoneName: str
    startDestination: Destination
    endDestination: Destination
    gotPoints: int
    length: float
    isOpen: bool = True

    def __hash__(self) -> int:
        return self.id
