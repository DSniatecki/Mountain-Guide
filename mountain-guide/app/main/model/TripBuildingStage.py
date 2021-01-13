from typing import List

from pydantic.main import BaseModel

from .TripSection import TripSection


class TripBuildingStage(BaseModel):
    totalGotPoints: int
    totalLengthKM: float
    sections: List[TripSection] = []
    possibleNextSections: List[TripSection] = []
